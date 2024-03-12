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
