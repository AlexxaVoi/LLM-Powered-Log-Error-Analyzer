from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=15)
    email: EmailStr
    # password: str = Field(..., min_length=8)


class UserReadSchema(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
