from mexc_api.types.base_schema import BaseSchema


class ApiResponse(BaseSchema):
    response: dict | list
    status_code: int
