import api.models.base as base


class CreatePage(base.BaseModel):
    url: str
    title: str
    content: str
