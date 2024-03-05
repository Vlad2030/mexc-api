from pydantic import BaseModel


class ApiResponse(BaseModel):
    response: dict | list
    status_code: int
