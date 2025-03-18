# bybit_p2p
## Bybit P2P API integration library written in Python

[![pip package](https://img.shields.io/pypi/v/bybit-p2p)](https://pypi.org/project/bybit-p2p/)

`bybit_p2p` is the official Python SDK for Bybit's P2P API, enabling seamless integration of your software solutions with Bybit's P2P trading platform.

- No need to implement signature (HMAC, RSA) logic yourself
- Easy & quick to work with
- Actively developed and maintained

*originally developed by kolya5544*

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
print(api.get_current_balance(accountType="FUND", coin="USDC"))

# 2. Get account information
print(api.get_account_information())

# 3. Get ads list
print(api.get_ads_list())
```

`P2P()` class is used for P2P API interactions. Here, `testnet` refers to environment. For Mainnet (https://bybit.com/), you shall use `testnet=False`. For Testnet (https://testnet.bybit.com/), use `testnet=True` instead.

RSA users should also set `rsa=True` in the constructor. TR/KZ/NL/etc. users can manipulate `domain` and `tld` parameters, like `tld="kz"`.

You can find the complete Quickstart example here: [bybit_p2p quickstart](https://github.com/bybit-exchange/bybit_p2p/blob/master/examples/quickstart.py).

## Documentation

bybit_p2p library currently consists of just one module, which is used for direct REST API requests to Bybit P2P API.

You can access P2P API documentation using this link: [Not Available at this moment in time](https://google.com/)

Here is a breakdown of how API methods correspond to appropriate bybit_p2p methods:

Advertisements:
| bybit_p2p method name | P2P API method name | P2P API endpoint path |
| --- | --- | --- |
| get_online_ads() | Get Market Online Ads list | [/v5/p2p/item/online](https://bybit-exchange.github.io/docs/p2p/ad/online-ad-list) |
| post_new_ad() | Post New Ad | [/v5/p2p/item/create](https://bybit-exchange.github.io/docs/p2p/ad/post-new-ad) |
| remove_ad() | Remove ad | [/v5/p2p/item/cancel](https://bybit-exchange.github.io/docs/p2p/ad/remove-ad) |
| update_ad() | Update / Relist My Ad | [/v5/p2p/item/update](https://bybit-exchange.github.io/docs/p2p/ad/update-list-ad) |
| get_ads_list() | Get ads list | [/v5/p2p/item/personal/list](https://bybit-exchange.github.io/docs/p2p/ad/ad-list) |
| get_ad_details() | Get ad detail | [/v5/p2p/item/info](https://bybit-exchange.github.io/docs/p2p/ad/ad-detail) |

Orders:
| bybit_p2p method name | P2P API method name | P2P API endpoint path |
| --- | --- | --- |
| get_orders() | Get All Orders | [/v5/p2p/order/simplifyList](https://bybit-exchange.github.io/docs/p2p/order/order-list) |
| get_order_details() | Get Order Details | [/v5/p2p/order/info](https://bybit-exchange.github.io/docs/p2p/order/order-detail) |
| get_pending_orders() | Get Pending Orders | [/v5/p2p/order/pending/simplifyList](https://bybit-exchange.github.io/docs/p2p/order/pending-order) |
| mark_as_paid() | Mark Order As Paid | [/v5/p2p/order/pay](https://bybit-exchange.github.io/docs/p2p/order/mark-order-as-paid) |
| release_assets() | Release Digital Asset | [/v5/p2p/order/finish](https://bybit-exchange.github.io/docs/p2p/order/release-digital-asset) |
| send_chat_message() | Send chat message | [/v5/p2p/order/message/send](https://bybit-exchange.github.io/docs/p2p/order/send-chat-msg) |
| upload_chat_file() | Upload chat file | [/v5/p2p/oss/upload_file](https://bybit-exchange.github.io/docs/p2p/order/upload-chat-file) |
| get_chat_messages() | Get Chat Message | [/v5/p2p/order/message/listpage](https://bybit-exchange.github.io/docs/p2p/order/chat-msg) |


User:
| bybit_p2p method name | P2P API method name | P2P API endpoint path |
| --- | --- | --- |
| get_account_information() | Get Account Information | [/v5/p2p/user/personal/info](https://bybit-exchange.github.io/docs/p2p/user/acct-info) |
| get_counterparty_info() | Get Counterparty User Info | [/v5/p2p/user/order/personal/info](https://bybit-exchange.github.io/docs/p2p/user/counterparty-user-info) |
| get_user_payment_types() | Get User Payment | [/v5/p2p/user/payment/list](https://bybit-exchange.github.io/docs/p2p/user/user-payment) |

Misc:
| bybit_p2p method name | P2P API method name | P2P API endpoint path |
| --- | --- | --- |
| get_current_balance() | Get Coin Balance | [/v5/asset/transfer/query-account-coins-balance](https://bybit-exchange.github.io/docs/p2p/all-balance) |

More methods will come soon, allowing for more advanced operations.

## Development

All contributions are welcome.

## License

MIT
