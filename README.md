# bybit_p2p
## Bybit P2P API integration library written in Python

[![pip package](https://img.shields.io/pypi/v/bybit-p2p)](https://pypi.org/project/bybit-p2p/)

`bybit_p2p` is the official Python SDK for Bybit's P2P API, enabling seamless integration of your software solutions with Bybit's P2P trading platform.

- No need to implement signature (HMAC, RSA) logic yourself
- Easy & quick to work with
- Actively developed and maintained

## Features

bybit_p2p currently implements all methods available for P2P API. The library is in active development, so any newly released features will be added almost immediately. Here is a short list of what the library can do:

- Create, edit, delete, activate advertisements
- Get pending orders, mark orders as paid, release assets to the buyer
- Get and send text messages, upload files and send files to the chat
- Get all public advertisements for tokens
- ...and so much else! 🌟

All features are usually one method call away and do not require advanced API understanding to interact with.

## Tech

bybit_p2p uses a number of projects and technologies to work:

- `requests` & `requests_toolbelt` for HTTP request creation and processing, as well as multiform data requests
- `PyCrypto` for HMAC and RSA operations

## Installation

`bybit_p2p` was tested on Python 3.11, but should work on all higher versions as well. The module can be installed manually or via [PyPI](https://pypi.org/project/pybit/) with `pip`:
```
pip install bybit-p2p
```

## Usage

Upon installation, you can use bybit_p2p by importing it in your code:
```
from bybit_p2p import P2P
```

Here is a quickstart example to get some info from the exchange:
```
from bybit_p2p import P2P

api = P2P(
    testnet=True,
    api_key="x",
    api_secret="x"
)

# 1. Get current balance
print(api.get_current_balance(accountType="UNIFIED"))

# 2. Get account information
print(api.get_account_information())

# 3. Get ads list
print(api.get_ads_list())
```

`P2P()` class is used for P2P API interactions. Here, `testnet` refers to environment. For Mainnet (https://bybit.com/), you shall use `testnet=False`. For Testnet (https://testnet.bybit.com/), use `testnet=True` instead.

RSA users should also set `rsa=True` in the constructor. TR/KZ/NL/etc. users can manipulate `domain` and `tld` parameters, like `tld="kz"`.

You can find the complete Quickstart example here: [bybit_p2p quickstart](https://github.com/kolya5544/bybit_p2p/blob/master/examples/quickstart.py).

## Documentation

bybit_p2p library currently consists of just one module, which is used for direct REST API requests to Bybit P2P API.

You can access P2P API documentation using this link: [Not Available at this moment in time](https://google.com/)

Here is a breakdown of how API methods correspond to appropriate bybit_p2p methods:
| bybit_p2p method name | P2P API method name | P2P API endpoint path |
| --- | --- | --- |
| get_current_balance() | Get current balance | [/v5/asset/transfer/query-account-coins-balance](https://bybit-exchange.github.io/docs/v5/asset/balance/all-balance) |
| get_account_information() | Get account information | /v5/p2p/user/personal/info |
| get_ads_list() | Get ads list | /v5/p2p/item/personal/list |
| get_ad_detail() | Get ad detail | /v5/p2p/item/info |
| update_ad() | Update/reOnline ads | /v5/p2p/item/update |
| offline_ad() | Offline ads | /v5/p2p/item/cancel |
| get_orders() | Get orders | /v5/p2p/order/simplifyList |
| get_pending_orders() | Get pending orders | /v5/p2p/order/pending/simplifyList |
| get_user_order_statistics() | Get user's order statistic | /v5/p2p/user/order/personal/info |
| get_order_details() | Get order detail | /v5/p2p/order/info |
| release_assets() | Release digital asset | /v5/p2p/order/finish |
| mark_as_paid() | Mark order as paid | /v5/p2p/order/pay |
| get_chat_messages() | Get chat message | /v5/p2p/order/message/list |
| upload_chat_file() | Upload chat file | /v5/p2p/oss/upload_file |
| send_chat_message() | Send chat message | /v5/p2p/order/message/send |
| post_new_ad() | post new ad | /v5/p2p/item/create |
| get_online_ads() | online Ad list | /v5/p2p/item/online |
| get_user_payment_types() | Get user payment | /v5/p2p/user/payment/list |

More modules will come soon, allowing for more advanced operations.

## Development

Contributions are welcome, non-breaking changes to the code are preferred.

## License

MIT
