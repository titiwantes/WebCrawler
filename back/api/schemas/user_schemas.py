from typing import Optional

import api.models.base as base


class UserCreate(base.BaseModel):
    pass


class UserCreateOut(base.BaseModel):
    id: int
    email: str
    name: str


class UserUpdate(base.BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
