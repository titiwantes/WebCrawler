import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql

import api.models.base as base


class Word(base.Base):

    __tablename__ = "words"
    id = sa.Column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
        unique=True,
    )

    word = sa.Column(mysql.VARCHAR(255), unique=True)
