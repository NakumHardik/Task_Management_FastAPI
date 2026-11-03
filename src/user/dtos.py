from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    username: str
    password: str
    email: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    email: str


class LoginSchema(BaseModel):
    username: str
    password: str
