from ._p2p_manager import P2PManager
from ._p2p_helper import P2PMethods


class P2PRequests(P2PManager):
    def get_current_balance(self, **kwargs):
        """
        Obtain wallet balance, query asset information of each currency.
        By default, currency information with assets or liabilities of 0 is not returned.

        :key accountType: Account type, UNIFIED
        :returns: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_CURRENT_BALANCE,
            params=kwargs
        )

    def get_account_information(self, **kwargs):
        """
        Get Account Information

        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_ACCOUNT_INFORMATION,
            params=kwargs
        )

    def get_ads_list(self, **kwargs):
        """
        Get Ads List

        :key itemId: Advertisement ID
        :key status: 1 - Sold out, 2 - Available
        :key side: 0 - Buy, 1 - Sell
        :key tokenId: Token ID, e.g.: USDT,BTC,ETH
        :key page: Page number, default is 1
        :key size: Page size, default is 10
        :key currency_id: Currency ID, e.g.: HKD,USD,EUR
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_ADS_LIST,
            params=kwargs
        )

    def get_ad_details(self, **kwargs):
        """
        Get Ad Details

        :key itemId: Advertisement ID
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_AD_DETAILS,
            params=kwargs
        )

    def update_ad(self, **kwargs):
        """
        Update or activate ads

        :key id: Advertisement ID
        :key priceType: 0 - fixed rate, 1 - floating rate
        :key premium: Floating ratio
        :key price: Advertisement price
        :key minAmount: Min.TX amount
        :key maxAmount: Max.TX amount
        :key remark: Advertisement description, up to 900 chars
        :key tradingPreferenceSet: [object] Trading Preferences
        :key paymentIds: [array str] Payment methods
        :key actionType: MODIFY to modify ad, ACTIVE to make ad active again
        :key quantity: Quantity
        :key paymentPeriod: Payment duration - 15 or 30, usually
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.UPDATE_AD,
            params=kwargs
        )

    def remove_ad(self, **kwargs):
        """
        Remove ad

        :key itemId: Advertisement ID
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.REMOVE_AD,
            params=kwargs
        )

    def get_orders(self, **kwargs):
        """
        Get orders

        :key status: Order Status
        :key beginTime: Begin Time
        :key endTime: End Time
        :key tokenId: Token ID
        :key side: [array int] Side
        :key page: Page number
        :key size: Rows per page
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_ORDERS,
            params=kwargs
        )

    def get_pending_orders(self, **kwargs):
        """
        Get pending orders

        :key status: Order Status
        :key beginTime: Begin Time
        :key endTime: End Time
        :key tokenId: Token ID
        :key side: [array int] Side
        :key page: Page number
        :key size: Rows per page
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_PENDING_ORDERS,
            params=kwargs
        )

    def get_counterparty_info(self, **kwargs):
        """
        Get counterparty info

        :key originalUid: Counterparty UID
        :key orderId: Order ID
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_COUNTERPARTY_INFO,
            params=kwargs
        )

    def get_order_details(self, **kwargs):
        """
        Get order details

        :key orderId: Order ID
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_ORDER_DETAILS,
            params=kwargs
        )

    def release_assets(self, **kwargs):
        """
        Release digital asset

        :key orderId: Order ID
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.RELEASE_ASSETS,
            params=kwargs
        )

    def mark_as_paid(self, **kwargs):
        """
        Mark order as paid

        :key orderId: Order ID
        :key paymentType: Payment method used. Located in paymentTermList -> paymentType
        :key paymentId: Payment method ID used. Located in paymentTermList -> id
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.MARK_AS_PAID,
            params=kwargs
        )

    def get_chat_messages(self, **kwargs):
        """
        Get chat messages

        :key orderId: Order ID
        :key startMessageId: Start message ID to query from
        :key size: Rows per query
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_CHAT_MESSAGES,
            params=kwargs
        )

    def upload_chat_file(self, **kwargs):
        """
        Upload file for chats

        :key upload_file: File to upload. Can be a string path, binary data, etc.
        :key filename: Sets filename. Default to the string path provided in `upload_file`.
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.UPLOAD_CHAT_FILE,
            params=kwargs
        )

    def send_chat_message(self, **kwargs):
        """
        Send chat message

        :key message: Chat message. For `str`, it's text contents. For `pic`, `pdf`, `video`, it's the URL
        :key contentType: One of the next values: str, pic, pdf, video
        :key orderId: Order ID
        :key msgUuid: Client message UUID
        :key fileName: Filename of the pic, pdf or video.
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.SEND_CHAT_MESSAGE,
            params=kwargs
        )

    def post_new_ad(self, **kwargs):
        """
        Post new advertisement

        :key tokenId: Token ID, like USDT, ETH, BTC
        :key currencyId: Currency ID, like RUB, USD, EUR
        :key side: 0 - buy, 1 - sell
        :key priceType: 0 - fixed rate, 1 - floating rate
        :key premium: Floating ratio
        :key price: Advertisement price
        :key minAmount: Min.TX amount
        :key maxAmount: Max.TX amount
        :key remark: Advertisement description, up to 900 chars
        :key tradingPreferenceSet: [object] Trading Preferences
        :key paymentIds: [array str] Payment methods
        :key quantity: Quantity
        :key paymentPeriod: Payment duration - 15 or 30, usually
        :key itemType: ORIGIN - original P2P ad, generally refers to non-bulk advertisement, BULK - bulk advertisement
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.POST_NEW_AD,
            params=kwargs
        )

    def get_online_ads(self, **kwargs):
        """
        Online advertisements list

        :key tokenId: Token ID, like USDT, ETH, BTC
        :key currencyId: Currency ID, like RUB, USD, EUR
        :key side: 0 - buy, 1 - sell
        :key page: Page number
        :key size: Rows per page
        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_ONLINE_ADS,
            params=kwargs
        )

    def get_user_payment_types(self, **kwargs):
        """
        Get user payment types

        :return: Response dictionary
        """

        return self.http_req_handler(
            method=P2PMethods.GET_USER_PAYMENT_TYPES,
            params=kwargs
        )