from mexc_api.enums import OrderSide, OrderType, OrderStatus
from mexc_api.types.base_schema import BaseSchema

class UserApiDefaultSymbol(BaseSchema):
    code: int
    data: list[str]
    msg: str | None


class NewOrder(BaseSchema):
    symbol: str
    order_id: str
    order_list_id: int
    price: str
    orig_qty: str
    type: str
    side: str
    transact_time: int


class Order(BaseSchema):
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: float | None = None
    quote_order_qty: float | None = None
    price: float | None = None
    order_id: str = None
    orig_client_order_id: str | None = None
    new_client_order_id: str | None = None


class BatchOrders(BaseSchema):
    symbol: str | None
    order_id: str | None
    order_list_id: int | None
    new_client_order_list_id: str | None
    msg: str | None
    code: int | None


class CancelOrder(BaseSchema):
    symbol: str
    orig_client_order_id: str
    order_id: int 
    client_order_id: str
    price: str
    orig_qty: str
    executed_qty: str
    commulative_quote_qty: str
    status: OrderStatus
    time_in_force: str
    type: OrderType
    side: OrderSide

