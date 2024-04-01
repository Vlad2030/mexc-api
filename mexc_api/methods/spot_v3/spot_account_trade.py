import orjson

from mexc_api.clients.mexc import MEXCClient
from mexc_api.enums import OrderSide, OrderType
from mexc_api.types.spot_account_trade import (
    UserApiDefaultSymbol,
    Order,
    NewOrder,
    BatchOrders,
    CancelOrder,
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
            order: Order,
    ) -> dict:
        params_dict = {}

        params_dict["symbol"] = order.symbol
        params_dict["side"] = order.side
        params_dict["type"] = order.type

        if order.quantity is not None:
            params_dict["quantity"] = order.quantity

        if order.quote_order_qty is not None:
            params_dict["quoteOrderQty"] = order.quote_order_qty

        if order.price is not None:
            params_dict["price"] = order.price

        if order.new_client_order_id is not None:
            params_dict["newClientOrderId"] = order.quote_order_qty

        params_dict["recvWindow"] = self.recv_window
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
            order: Order,
    ) -> dict:
        params_dict = {}

        params_dict["symbol"] = order.symbol
        params_dict["side"] = order.side
        params_dict["type"] = order.type

        if order.quantity is not None:
            params_dict["quantity"] = order.quantity

        if order.quote_order_qty is not None:
            params_dict["quoteOrderQty"] = order.quote_order_qty

        if order.price is not None:
            params_dict["price"] = order.price

        if order.new_client_order_id is not None:
            params_dict["newClientOrderId"] = order.quote_order_qty

        params_dict["recvWindow"] = self.recv_window
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

    async def batch_orders(
            self,
            batch_orders: list[Order],
            order: Order,
    ) -> BatchOrders | list[BatchOrders]:
        batch_orders_list = []
        params_dict = {}

        if len(batch_orders) > 20:
            raise ValueError("list of batch_orders must be less than 20 orders")

        params_dict["batchOrders"] = (
            orjson.dumps(
                "["
                + "".join([batch_order.model_dump_json() for batch_order in batch_orders])
                + "]"
            )
            .decode()
            .replace("\\", ""),
        )   # dont judge me for this shit code, its the most better solution xD
        params_dict["symbol"] = order.symbol
        params_dict["side"] = order.side
        params_dict["type"] = order.type

        if order.quantity is not None:
            params_dict["quantity"] = order.quantity

        if order.quote_order_qty is not None:
            params_dict["quoteOrderQty"] = order.quote_order_qty

        if order.price is not None:
            params_dict["price"] = order.price

        if order.new_client_order_id is not None:
            params_dict["newClientOrderId"] = order.quote_order_qty

        params_dict["timestamp"] = self.client.timestamp()
        params_dict["signature"] = self.client.signature(
            message=self.client.urlencode(params_dict),
            secret=self.api_secret,
        )

        request = await self.client.request(
            method="POST",
            endpoint="/api/v3/batchOrders",
            params=params_dict,
        )

        if isinstance(request.response, list):
            for batch_order in request.response:
                batch_orders_list.append(BatchOrders(**to_snake_case(batch_order)))

            return batch_orders_list

        return BatchOrders(**to_snake_case(request.response))

    async def cancel_order(
            self,
            order: Order,
    ) -> CancelOrder:
        params_dict = {}

        params_dict["symbol"] = order.symbol

        if order.order_id is not None:
            params_dict["orderId"] = order.order_id

        if order.orig_client_order_id is not None:
            params_dict["origClientOrderId"] = order.orig_client_order_id

        if order.new_client_order_id is not None:
            params_dict["newClientOrderId"] = order.quote_order_qty

        params_dict["recvWindow"] = self.recv_window
        params_dict["timestamp"] = self.client.timestamp()
        params_dict["signature"] = self.client.signature(
            message=self.client.urlencode(params_dict),
            secret=self.api_secret,
        )

        request = await self.client.request(
            method="DELETE",
            endpoint="/api/v3/order",
            params=params_dict,
        )

        return CancelOrder(**to_snake_case(request.response))

    async def cancel_all_open_orders_on_a_symbol(
            self,
            symbol: str | list[str],
    ) -> CancelOrder | list[CancelOrder]:
        cancel_order_list = []
        params_dict = {}

        if isinstance(symbol, list):
            if len(symbol) > 5:
                ValueError("list symbol must be less than 5 symbols")

            symbol = ",".join(symbol)

        params_dict["symbol"] = symbol

        params_dict["recvWindow"] = self.recv_window
        params_dict["timestamp"] = self.client.timestamp()
        params_dict["signature"] = self.client.signature(
            message=self.client.urlencode(params_dict),
            secret=self.api_secret,
        )

        request = await self.client.request(
            method="DELETE",
            endpoint="/api/v3/openOrders",
            params=params_dict,
        )

        if isinstance(request.response, list):
            for cancel_order in request.response:
                cancel_order_list.append(CancelOrder(**to_snake_case(cancel_order)))

            return cancel_order_list

        return CancelOrder(**to_snake_case(request.response))






