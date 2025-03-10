import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql

import api.models.base as base


class Page_word(base.Base):

    __tablename__ = "pages_words"
    id = sa.Column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    page_id = sa.Column(
        mysql.BIGINT(unsigned=True),
        sa.ForeignKey("pages.id", ondelete="CASCADE"),
        nullable=False,
    )

    word_id = sa.Column(
        mysql.BIGINT(unsigned=True),
        sa.ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
    )
