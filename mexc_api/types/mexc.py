from mexc_api.types.base_schema import BaseSchema


class MexcApiError(BaseSchema):
    msg: str
    code: int
    _extend: str | None
