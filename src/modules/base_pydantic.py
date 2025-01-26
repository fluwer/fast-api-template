from pydantic import BaseModel
from pydantic import ConfigDict


class BasePydanticModel(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )
