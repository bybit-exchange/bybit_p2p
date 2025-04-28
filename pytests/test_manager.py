import logging

import pytest
import sys
import os

import requests

# Add the local library path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../bybit_p2p')))

# Now you can import your local library
from bybit_p2p import P2P


def test_generate_payload_get():
    payload = P2P._generate_payload("GET", {"b": 2, "a": 1})
    assert payload == "a=1&b=2"


def test_generate_payload_post():
    payload = P2P._generate_payload("POST", {"amount": 10})
    assert payload == '{"amount": 10}'


def test_sign_hmac():
    sig = P2P._sign(False, "secret", "some_string")
    assert isinstance(sig, str)
    assert len(sig) == 64  # длина SHA256 hex


def test_init_network():
    # Test for Testnet
    manager_testnet = P2P(testnet=True, api_key="dummy", api_secret="dummy")
    manager_testnet._init_network()
    assert manager_testnet._subdomain == "api-testnet"
    assert manager_testnet._url == "https://api-testnet.bybit.com"

    # Test for Mainnet
    manager_mainnet = P2P(testnet=False, api_key="dummy", api_secret="dummy")
    manager_mainnet._init_network()
    assert manager_mainnet._subdomain == "api"
    assert manager_mainnet._url == "https://api.bybit.com"


def test_init_http_client():
    # Test with SSL checks enabled
    manager_ssl = P2P(testnet=True, api_key="dummy", api_secret="dummy", disable_ssl_checks=False)
    manager_ssl._init_http_client()
    assert isinstance(manager_ssl.client, requests.Session)
    assert manager_ssl.client.verify is True
    assert manager_ssl.client.headers["Content-Type"] == "application/json"

    # Test with SSL checks disabled
    manager_no_ssl = P2P(testnet=True, api_key="dummy", api_secret="dummy", disable_ssl_checks=True)
    manager_no_ssl._init_http_client()
    assert manager_no_ssl.client.verify is False


def test_init_logger():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Test logger initialization
    manager = P2P(testnet=True, api_key="dummy", api_secret="dummy", logging_level=logging.WARN)
    manager._init_logger()

    # Check that logger is set up correctly
    assert isinstance(manager.logger, logging.Logger)

    # Check that a handler has been added
    assert len(manager.logger.handlers) > 0
    assert isinstance(manager.logger.handlers[0], logging.StreamHandler)

    # Check the log level
    assert manager.logger.level == logging.WARN