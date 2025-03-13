import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql

import api.models.base as base


class Page(base.Base):

    __tablename__ = "pages"
    id = sa.Column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    url = sa.Column(
        mysql.TEXT,
        nullable=False,
    )

    title = sa.Column(
        sa.TEXT,
    )

    content = sa.Column(
        mysql.LONGTEXT,
        nullable=False,
    )

    incoming_links = sa.Column(
        sa.Integer, nullable=False, default=0, server_default="0"
    )

    words_count = sa.Column(
        mysql.BIGINT(unsigned=True), nullable=False, default=0, server_default="0"
    )

    last_crawled = sa.Column(
        sa.TIMESTAMP,
        nullable=False,
        default=sa.func.now(),
        onupdate=sa.func.now(),
        server_default=sa.func.now(),
    )
