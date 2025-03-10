import uuid

import api.models.base as base


class UserAuthDataCreate(base.BaseModel):
    user_id: int
    email: str
    name: str
    password_hash: str
    is_validated: bool = False
