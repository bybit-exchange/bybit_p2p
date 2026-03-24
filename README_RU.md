# bybit_p2p

## Библиотека интеграции с Bybit P2P API, написанная на Python

[![pip package](https://img.shields.io/pypi/v/bybit-p2p)](https://pypi.org/project/bybit-p2p/)

`bybit_p2p` - официальный Python SDK для P2P API Bybit, обеспечивающий интеграцию ваших программных решений с [P2P-платформой Bybit](https://www.bybit.com/en/promo/global/p2p-introduce).

-   Нет необходимости самостоятельно реализовывать логику подписи запросов на сервер (HMAC, RSA)
-   Прост и быстр в использовании
-   Активно развивается и поддерживается

_изначально разработан kolya5544_

## Возможности

bybit_p2p в настоящее время реализует все методы, доступные в P2P API. Библиотека находится в активной разработке, поэтому любые новые функции добавляются почти сразу. Ниже краткий список того, что умеет библиотека:

-   Создание, редактирование, удаление, активация объявлений
-   Получение ожидающих ордеров, отметка ордеров как оплаченных, выпуск активов покупателю
-   Получение и отправка текстовых сообщений, загрузка файлов и отправка файлов в чат
-   Получение всех публичных объявлений
-   ...и многое другое! 🌟

Все функции обычно доступны одним вызовом метода и не требуют углублённого понимания API для взаимодействия.

## Технологии

bybit_p2p использует ряд проектов и технологий:

-   `requests` и `requests_toolbelt` для создания и обработки HTTP-запросов, а также запросов с мультиформ-данными
-   `PyCrypto` для операций HMAC и RSA

## Установка

`bybit_p2p` тестировался на Python 3.11, но должен работать и на всех более новых версиях. Модуль можно установить вручную или через [PyPI](https://pypi.org/project/bybit_p2p/) с помощью `pip`:

```
pip install bybit-p2p
```

## Использование

После установки вы можете использовать bybit_p2p, импортировав его в код:

```
from bybit_p2p import P2P
```

Вот пример кода:

```
from bybit_p2p import P2P

api = P2P(
    testnet=True,
    api_key="x",
    api_secret="x"
)

# 1. Получить текущий баланс
print(api.get_current_balance(accountType="FUND", coin="USDC"))

# 2. Получить информацию об аккаунте
print(api.get_account_information())

# 3. Получить список объявлений
print(api.get_ads_list())
```

Класс `P2P()` используется для взаимодействия с P2P API. Здесь `testnet` означает окружение. Для Мейннета ([https://bybit.com/](https://bybit.com/)) следует использовать `testnet=False`. Для Тестнета ([https://testnet.bybit.com/](https://testnet.bybit.com/)) используйте `testnet=True`.

Пользователям RSA также следует установить `rsa=True` в конструкторе. Пользователи TR/KZ/NL/и т. д. могут изменять параметры `domain` и `tld`, например `tld="kz"`.

Полный пример кода доступен здесь: [bybit_p2p quickstart](https://github.com/bybit-exchange/bybit_p2p/blob/master/examples/quickstart.py).

## Документация

Библиотека bybit_p2p в настоящее время состоит всего из одного модуля, который используется для прямых REST-запросов к P2P API Bybit.

Получить доступ к документации P2P API можно по ссылке: [P2P API documentation](https://bybit-exchange.github.io/docs/p2p/guide)

Ниже приведено соответствие методов API методам bybit_p2p:

Объявления:

| имя метода bybit_p2p | имя метода P2P API                    | Путь эндпоинта P2P API                                                             |
| -------------------- | ------------------------------------- | ---------------------------------------------------------------------------------- |
| get_online_ads()     | Получить все объявления               | [/v5/p2p/item/online](https://bybit-exchange.github.io/docs/p2p/ad/online-ad-list) |
| post_new_ad()        | Создать новое объявление              | [/v5/p2p/item/create](https://bybit-exchange.github.io/docs/p2p/ad/post-new-ad)    |
| remove_ad()          | Убрать объявление                     | [/v5/p2p/item/cancel](https://bybit-exchange.github.io/docs/p2p/ad/remove-ad)      |
| update_ad()          | Обновить либо активировать объявление | [/v5/p2p/item/update](https://bybit-exchange.github.io/docs/p2p/ad/update-list-ad) |
| get_ads_list()       | Получить свои объявление              | [/v5/p2p/item/personal/list](https://bybit-exchange.github.io/docs/p2p/ad/ad-list) |
| get_ad_details()     | Получить детали своего объявления     | [/v5/p2p/item/info](https://bybit-exchange.github.io/docs/p2p/ad/ad-detail)        |

Ордера:

| имя метода bybit_p2p | имя метода P2P API                        | Путь эндпоинта P2P API                                                                              |
| -------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------- |
| get_orders()         | Получить все ордера                       | [/v5/p2p/order/simplifyList](https://bybit-exchange.github.io/docs/p2p/order/order-list)            |
| get_order_details()  | Получить информацию по ордеру             | [/v5/p2p/order/info](https://bybit-exchange.github.io/docs/p2p/order/order-detail)                  |
| get_pending_orders() | Получить открытые ордера                  | [/v5/p2p/order/pending/simplifyList](https://bybit-exchange.github.io/docs/p2p/order/pending-order) |
| mark_as_paid()       | Отметить ордер как оплаченный             | [/v5/p2p/order/pay](https://bybit-exchange.github.io/docs/p2p/order/mark-order-as-paid)             |
| release_assets()     | Отпустить средства контрагенту            | [/v5/p2p/order/finish](https://bybit-exchange.github.io/docs/p2p/order/release-digital-asset)       |
| send_chat_message()  | Отправить сообщение в чат                 | [/v5/p2p/order/message/send](https://bybit-exchange.github.io/docs/p2p/order/send-chat-msg)         |
| upload_chat_file()   | Залить файл для дальнейшей отправки в чат | [/v5/p2p/oss/upload_file](https://bybit-exchange.github.io/docs/p2p/order/upload-chat-file)         |
| get_chat_messages()  | Получить сообщения в чате                 | [/v5/p2p/order/message/listpage](https://bybit-exchange.github.io/docs/p2p/order/chat-msg)          |

Пользователь:

| имя метода bybit_p2p      | имя метода P2P API                         | Путь эндпоинта P2P API                                                                                    |
| ------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| get_account_information() | Получить информацию о текущем пользователе | [/v5/p2p/user/personal/info](https://bybit-exchange.github.io/docs/p2p/user/acct-info)                    |
| get_counterparty_info()   | Получить информацию о контрагенте          | [/v5/p2p/user/order/personal/info](https://bybit-exchange.github.io/docs/p2p/user/counterparty-user-info) |
| get_user_payment_types()  | Получить доступные методы оплаты           | [/v5/p2p/user/payment/list](https://bybit-exchange.github.io/docs/p2p/user/user-payment)                  |

Разное:

| имя метода bybit_p2p  | имя метода P2P API    | Путь эндпоинта P2P API                                                                                  |
| --------------------- | --------------------- | ------------------------------------------------------------------------------------------------------- |
| get_current_balance() | Получить баланс монет | [/v5/asset/transfer/query-account-coins-balance](https://bybit-exchange.github.io/docs/p2p/all-balance) |

По мере необходимости будут появляться дополнительные методы, позволяющие выполнять более продвинутые операции.

## Лицензия

MIT
