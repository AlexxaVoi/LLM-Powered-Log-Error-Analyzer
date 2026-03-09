from pydantic import BaseModel


class Base(BaseModel):
    pass


class User(Base):
    user: str
    email: str
