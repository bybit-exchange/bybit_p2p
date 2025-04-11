import base64
import hashlib
import hmac
import json
import os

import requests
import logging
import time
from datetime import datetime as dt, timezone
from json import JSONDecodeError
from requests_toolbelt import MultipartEncoder

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from ._exceptions import FailedRequestError
from ._p2p_method import P2PMethod

_SUBDOMAIN_TESTNET = "api-testnet"
_SUBDOMAIN_MAINNET = "api"
_DOMAIN_MAIN = "bybit"
_DOMAIN_ALT = "bytick"
_TLD_MAIN = "com"


class P2PManager:
    def __init__(
            self,
            testnet,
            api_key="",
            api_secret="",
            domain=None,
            tld=None,
            recv_window=5000,
            rsa=False,
            logging_level=logging.INFO,
            disable_ssl_checks=False
    ):
        self._testnet = testnet
        self._api_key = api_key
        self._api_secret = api_secret
        self._domain = domain or _DOMAIN_MAIN
        self._tld = tld or _TLD_MAIN
        self._recv_window = recv_window
        self._rsa = rsa
        self._logging_level = logging_level
        self._disable_ssl_checks = disable_ssl_checks

        # Set network settings: URL, subdomain, and environment
        self._init_network()

        # Create HTTP session with necessary headers and SSL settings
        self._init_http_client()

        # Set up logging if not already configured
        self._init_logger()

        self.logger.debug("Initialized P2P API session.")

    def _init_network(self):
        self._subdomain = _SUBDOMAIN_TESTNET if self._testnet else _SUBDOMAIN_MAINNET
        self._url = f"https://{self._subdomain}.{self._domain}.{self._tld}"

    def _init_http_client(self):
        self.client = requests.Session()
        self.client.verify = not self._disable_ssl_checks
        self.client.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _init_logger(self):
        self.logger = logging.getLogger(__name__)
        # Only attach a handler if no logging handlers exist yet
        if not logging.root.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            ))
            handler.setLevel(self._logging_level)
            self.logger.addHandler(handler)
        self.logger.setLevel(self._logging_level)

    def http_req_handler(self, method: P2PMethod, params):
        if params is None:
            params = {}

        self._validate_required_params(method, params)
        self._sanitize_params(params)

        timestamp = int(time.time() * 10 ** 3)

        # Prepare payload and content type based on request method
        if method.http_method == "FILE":
            payload, content_type, signature = self._handle_file_upload(method, params, timestamp)
        else:
            payload = self._generate_payload(method.http_method, params)
            content_type = "application/json"
            signature = self._generate_sign(payload, timestamp)

        headers = self._build_headers(signature, timestamp, content_type)
        request = self._prepare_request(method, payload, headers)
        response = self._send_request(request)
        return self._process_response(response, method, payload)

    def _validate_required_params(self, method, params):
        # Ensure all required parameters are passed
        missing_params = [p for p in method.required_params if p not in params]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    def _sanitize_params(self, params):
        # Fix for signature errors due to float-integer mismatches
        for i in params:
            if isinstance(params[i], float) and params[i] == int(params[i]):
                params[i] = int(params[i])

    def _handle_file_upload(self, method, params, timestamp):
        filepath = params["upload_file"]
        boundary = "boundary-for-file"
        content_type = f"multipart/form-data; boundary={boundary}"
        filename = os.path.basename(str(filepath))
        mime_type = "image/png"

        with open(filepath, "rb") as f:
            binary_data = f.read()

        files = MultipartEncoder(
            {
                'upload_file': (
                    filename,
                    open(filepath, "rb"),
                    mime_type
                )
            },
            boundary=boundary
        )

        payload = (
                      f"--{boundary}\r\n"
                      f"Content-Disposition: form-data; name=\"upload_file\"; filename=\"{filename}\"\r\nContent-Type: {mime_type}\r\n\r\n"
                  ).encode() + binary_data + f"\r\n--{boundary}--\r\n".encode()
        signature = self._generate_sign_binary(payload, timestamp)
        return files.to_string(), content_type, signature

    def _build_headers(self, signature, timestamp, content_type):
        return {
            'X-BAPI-API-KEY': self._api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': str(timestamp),
            'X-BAPI-RECV-WINDOW': str(self._recv_window),
            'Content-Type': content_type
        }

    def _prepare_request(self, method, payload, headers):
        endpoint = self._url + method.url
        if method.http_method == "GET":
            return self.client.prepare_request(
                requests.Request(
                    method.http_method, endpoint + f"?{payload}" if payload != "" else "", headers=headers
                )
            )
        else:
            return self.client.prepare_request(
                requests.Request(
                    "POST", endpoint, data=payload, headers=headers
                )
            )

    def _send_request(self, request):
        try:
            return self.client.send(request)
        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
        ) as e:
            raise e

    def _process_response(self, response, method, payload):
        # Handle HTTP error codes
        if response.status_code != 200:
            if response.status_code == 403:
                error_msg = ("Access denied error. Possible causes: 1) your IP is located in the US or Mainland China, "
                             "2) IP banned due to ratelimit violation")
            elif response.status_code == 401:
                error_msg = ("Unauthorized. Possible causes: 1) incorrect API key and/or secret, "
                             "2) incorrect environment: Mainnet vs Testnet")
            else:
                error_msg = f"HTTP status code is: {response.status_code}, expected: 200"
                self.logger.error(f"{error_msg}")
            raise FailedRequestError(
                request=f"{self._url + method.url}: {payload}",
                message=error_msg,
                status_code=response.status_code,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=response.headers,
            )

        try:
            s_json = response.json()
        except JSONDecodeError:
            self.logger.debug(f"Response text: {response.text}")
            raise FailedRequestError(
                request=f"{self._url + method.url}: {payload}",
                message="Could not decode JSON.",
                status_code=response.status_code,
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=response.headers,
            )

        ret_code = "retCode" if "retCode" in s_json else "ret_code"
        ret_msg = "retMsg" if "retMsg" in s_json else "ret_msg"

        if s_json[ret_code]:
            error_msg = f"{s_json[ret_msg]} (ErrCode: {s_json[ret_code]})"
            self.logger.error(f"{error_msg}")
            raise FailedRequestError(
                request=f"{self._url + method.url}: {payload}",
                message=s_json[ret_msg],
                status_code=s_json[ret_code],
                time=dt.now(timezone.utc).strftime("%H:%M:%S"),
                resp_headers=response.headers,
            )

        return s_json

    def _generate_sign(self, payload, timestamp):
        sign_string = str(timestamp) + self._api_key + str(self._recv_window) + payload
        return P2PManager._sign(self._rsa, self._api_secret, sign_string)

    def _generate_sign_binary(self, payload, timestamp):
        sign_string = f"{timestamp}{self._api_key}{self._recv_window}".encode() + payload
        return P2PManager._sign(self._rsa, self._api_secret, sign_string, True)

    # reference: https://github.com/bybit-exchange/pybit
    @staticmethod
    def _cast_values(params):
        str_params = [
            "itemId",
            "side",
            "currency_id",
            # get_ad_detail
            "id",
            "priceType",
            "premium",
            "price",
            "minAmount",
            "maxAmount",
            "remark",
            "actionType",
            "quantity",
            "paymentPeriod",
            # -> tradingPreferenceSet
            "hasUnPostAd",
            "isKyc",
            "isEmail",
            "isMobile",
            "hasRegisterTime",
            "registerTimeThreshold",
            "orderFinishNumberDay30",
            "completeRateDay30",
            "nationalLimit",
            "hasOrderFinishNumberDay30",
            "hasCompleteRateDay30",
            "hasNationalLimit",
            # get_orders
            "beginTime",
            "endTime",
            "tokenId",
            # get chat message
            "startMessageId"
        ]
        int_params = [
            "positionIdx",
        ]

        P2PManager._cast_dict_recursively(params, str_params, int_params)


    @staticmethod
    def _cast_dict_recursively(dictionary, str_params, int_params):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                # recursive edit
                P2PManager._cast_dict_recursively(value, str_params, int_params)
                continue

            if key in str_params:
                if not isinstance(value, str):
                    dictionary[key] = str(value)
            elif key in int_params:
                if not isinstance(value, int):
                    dictionary[key] = int(value)

    # reference: https://github.com/bybit-exchange/pybit
    @staticmethod
    def _generate_payload(http_method, params):
        if http_method == "GET":
            payload = "&".join(
                [
                    str(k) + "=" + str(v)
                    for k, v in sorted(params.items())
                    if v is not None
                ]
            )
            return payload
        elif http_method == "POST":
            P2PManager._cast_values(params)
            return json.dumps(params)


    # reference: https://github.com/bybit-exchange/pybit
    @staticmethod
    def _sign(use_rsa_authentication, secret, param_str, binary=False):
        def generate_hmac():
            hash = hmac.new(
                bytes(secret, "utf-8"),
                param_str.encode("utf-8"),
                hashlib.sha256,
            )
            return hash.hexdigest()

        def generate_hmac_binary():
            hash = hmac.new(
                bytes(secret, "utf-8"),
                param_str,
                hashlib.sha256,
            )
            return hash.hexdigest()

        def generate_rsa():
            hash = SHA256.new(param_str.encode("utf-8"))
            encoded_signature = base64.b64encode(
                PKCS1_v1_5.new(RSA.importKey(secret)).sign(
                    hash
                )
            )
            return encoded_signature.decode()

        def generate_rsa_binary():
            hash = SHA256.new(param_str)
            encoded_signature = base64.b64encode(
                PKCS1_v1_5.new(RSA.importKey(secret)).sign(
                    hash
                )
            )
            return encoded_signature.decode()

        if not use_rsa_authentication:
            if binary:
                return generate_hmac_binary()
            return generate_hmac()
        else:
            if binary:
                return generate_rsa_binary()
            return generate_rsa()

