import api.models.crawl_task as crawl_mdl
import api.crud.crawl_task_crud as crawl_crud
import db.sessions as db
from celery import Celery

app = Celery(
    "my_crawler", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

app.conf.result_expires = 3600


@app.task(name="my_crawler.crawl")
def crawl(url):
    try:
        writer = next(
            db.get_db_writer(db_url="mysql+mysqlconnector://user:password@db/db")
        )

        task = crawl_mdl.CrawlTask(status="RUNNING")
        return f"{crawl_crud.CrawlTaskCrud.create(writer, task).id}"
    except Exception as e:
        raise (e)
