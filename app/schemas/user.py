from pydantic import BaseModel, Field, ConfigDict


class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=15)
    password: str = Field(..., min_length=8)


class UserReadSchema(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
