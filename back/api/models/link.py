import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql

import api.models.base as base


class Link(base.Base):

    __tablename__ = "links"
    id = sa.Column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    from_page_id = sa.Column(
        mysql.BIGINT(unsigned=True),
        sa.ForeignKey("pages.id", ondelete="CASCADE"),
        nullable=False,
    )

    to_page_id = sa.Column(
        mysql.BIGINT(unsigned=True),
        sa.ForeignKey("pages.id", ondelete="CASCADE"),
        nullable=False,
    )
