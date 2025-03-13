import api.models.crawl_task as crawl_mdl
import api.crud.crawl_task_crud as crawl_crud
import db.sessions as db
import crawler.crawler as clr
from celery import Celery


app = Celery(
    "my_crawler", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

app.conf.result_expires = 3600


@app.task(name="my_crawler.crawl")
def crawl(urls: list[str]):
    if len(urls) == 0:
        raise ValueError("No urls to crawl")
    with db.get_dbs(db_url="mysql+mysqlconnector://user:password@db/db") as dbs:
        _, writer = dbs
        crawl_task = crawl_crud.CrawlTaskCrud.create(db=writer, seeds=urls)
        urls = set(urls)
        try:
            crawler = clr.Crawler(dbs=dbs, urls=urls, task_id=crawl_task.id)
            crawler.run()

        except Exception as e:
            crawl_crud.update_crawl_task_status(
                dbs[1], crawl_mdl.CrawlTaskStatus.FAILED
            )
            raise e
