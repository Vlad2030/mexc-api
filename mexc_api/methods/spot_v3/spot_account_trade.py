from mexc_api.clients.mexc import MEXCClient
from mexc_api.enums import OrderSide, OrderType
from mexc_api.types.spot_account_trade import (
    UserApiDefaultSymbol,
    NewOrder,
)
from mexc_api.clients.core.exceptions import MissingApiKey, MissingApiSecret
from mexc_api.utils.case import to_snake_case
from mexc_api.utils.case import to_snake_case


class SpotAccountTrade:
    def __init__(
            self,
            client: MEXCClient,
            recv_window: int = 5000,
    ) -> None:
        self.client = client
        self.recv_window = recv_window
        self.api_key = self.client.mexc_key
        self.api_secret = self.client.mexc_secret

        if self.api_key is None:
            raise MissingApiKey(f"Missing MEXC API key")

        if self.api_secret is None:
            raise MissingApiSecret(f"Missing MEXC API secret")

    async def __aenter__(self) -> "SpotAccountTrade":
        return self

    async def __aexit__(self) -> None:
        return await self.client.close_session()

    async def user_api_default_symbol(self) -> UserApiDefaultSymbol:
        params_dict = {}
        params_dict["timestamp"] = self.client.timestamp()
        params_dict["signature"] = self.client.signature(
            message=self.client.urlencode(params_dict),
            secret=self.api_secret,
        )

        request = await self.client.request(
            method="GET",
            endpoint="/api/v3/selfSymbols",
            params=params_dict,
        )

        return UserApiDefaultSymbol(**to_snake_case(request.response))

    async def test_new_order(
            self,
            symbol: str,
            side: OrderSide,
            type: OrderType,
            quantity: float = None,
            quote_order_qty: float = None,
            price: float = None,
            new_client_order_id: str = None,
    ) -> dict:
        params_dict = {}

        params_dict["symbol"] = symbol
        params_dict["side"] = side
        params_dict["type"] = type

        if quantity is not None:
            params_dict["quantity"] = quantity

        if quote_order_qty is not None:
            params_dict["quoteOrderQty"] = quote_order_qty

        if price is not None:
            params_dict["price"] = price

        if new_client_order_id is not None:
            params_dict["newClientOrderId"] = quote_order_qty

        params_dict["timestamp"] = self.client.timestamp()
        params_dict["signature"] = self.client.signature(
            message=self.client.urlencode(params_dict),
            secret=self.api_secret,
        )

        request = await self.client.request(
            method="POST",
            endpoint="/api/v3/order/test",
            params=params_dict,
        )

        return request.response

    async def new_order(
            self,
            symbol: str,
            side: OrderSide,
            type: OrderType,
            quantity: float = None,
            quote_order_qty: float = None,
            price: float = None,
            new_client_order_id: str = None,
    ) -> dict:
        params_dict = {}

        params_dict["symbol"] = symbol
        params_dict["side"] = side
        params_dict["type"] = type

        if quantity is not None:
            params_dict["quantity"] = quantity

        if quote_order_qty is not None:
            params_dict["quoteOrderQty"] = quote_order_qty

        if price is not None:
            params_dict["price"] = price

        if new_client_order_id is not None:
            params_dict["newClientOrderId"] = quote_order_qty

        params_dict["timestamp"] = self.client.timestamp()
        params_dict["signature"] = self.client.signature(
            message=self.client.urlencode(params_dict),
            secret=self.api_secret,
        )

        request = await self.client.request(
            method="POST",
            endpoint="/api/v3/order",
            params=params_dict,
        )

        return NewOrder(**to_snake_case(request.response))



