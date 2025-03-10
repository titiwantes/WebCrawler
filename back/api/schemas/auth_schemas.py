from pydantic import EmailStr

import api.models.base as base


class Login(base.BaseModel):
    email: str
    password: str


class LoginOut(base.BaseModel):
    email: str
    name: str
    id: int


class Signup(base.BaseModel):
    email: str
    name: str
    password: str
    password_confirm: str
