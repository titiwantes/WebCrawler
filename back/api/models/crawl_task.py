import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql

import api.models.base as base
import enum


class CrawlTaskStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class CrawlTask(base.Base):

    __tablename__ = "crawl_tasks"
    id = sa.Column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    status = sa.Enum(CrawlTaskStatus, nullable=False, default=CrawlTaskStatus.PENDING)

    start_time = sa.Column(
        sa.TIMESTAMP,
        nullable=False,
        default=sa.func.now(),
        onupdate=sa.func.now(),
        server_default=sa.func.now(),
    )

    end_time = sa.Column(
        sa.TIMESTAMP,
        nullable=True,
    )

    seeds = sa.Column(
        sa.JSON,
        nullable=False,
        default={},
    )

    error_message = sa.Column(
        sa.TEXT,
        nullable=True,
    )
