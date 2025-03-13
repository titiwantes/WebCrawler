import sqlalchemy as sa
import sqlalchemy.orm as orm
import api.models.crawl_task as crawl_mdl
import core.exeptions.exception as exceptions


class CrawlTaskCrud:
    @classmethod
    def create(cls, db: sa.orm.Session, seeds: list[str]) -> crawl_mdl.CrawlTask:
        crawl_task = crawl_mdl.CrawlTask(seeds=seeds)
        db.add(crawl_task)
        db.flush()
        db.refresh(crawl_task)
        return crawl_task

    @classmethod
    def update_status(
        cls, db: orm.Session, crawl_task_id: int, status: crawl_mdl.CrawlTaskStatus
    ) -> crawl_mdl.CrawlTask:
        crawl_task = (
            db.query(crawl_mdl.CrawlTask)
            .filter(crawl_mdl.CrawlTask.id == crawl_task_id)
            .first()
        )
        if not crawl_task:
            raise exceptions.NotFoundError("Crawl task not found")
        crawl_task.status = status
        db.flush()
        db.refresh(crawl_task)
        return crawl_task
