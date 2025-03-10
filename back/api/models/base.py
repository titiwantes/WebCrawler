import datetime

import pydantic
import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.sql.functions as sql

Base = declarative.declarative_base()


class BaseModel(pydantic.BaseModel):
    class Config:
        pass
