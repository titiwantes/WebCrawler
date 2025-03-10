import api.models.base as base


class ItemOut(base.BaseModel):
    id: int
    name: str
    description: str


class ItemCreate(base.BaseModel):
    name: str
    description: str
