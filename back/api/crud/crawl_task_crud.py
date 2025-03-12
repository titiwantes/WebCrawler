import sqlalchemy as sa
import api.models.crawl_task as crawl_mdl
import core.exeptions.exception as exceptions


class CrawlTaskCrud:
    @classmethod
    def create(
        cls, db: sa.orm.Session, task: crawl_mdl.CrawlTask
    ) -> crawl_mdl.CrawlTask:
        try:
            db.add(task)
            db.commit()
            db.refresh(task)
            return task
        except Exception as e:
            db.rollback()
            raise exceptions.InternalServerError(e)
