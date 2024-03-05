from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=None,
        populate_by_name=False,
        from_attributes=False,
    )
