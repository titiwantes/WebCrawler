import sqlalchemy as sa
import sqlalchemy.dialects.mysql as mysql

import api.models.base as base


class CrawlTask(base.Base):

    __tablename__ = "crawl_tasks"
    id = sa.Column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    status = sa.Enum(
        "PENDING",
        "RUNNING",
        "COMPLETED",
        "FAILED",
        name="crawl_task_status",
    )

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

    error_message = sa.Column(
        sa.TEXT,
        nullable=True,
    )
