import fastapi
import db.sessions as db
import api.services.page_services as page_srv
import api.schemas.page_schemas as page_sch
import core.celery as celery_app
import api.services.search_service as search_src

router = fastapi.APIRouter()


@router.post("/pages/create")
async def create(page: page_sch.CreatePage, dbs=fastapi.Depends(db.get_dbs)):
    return celery_app.crawl.delay(page.url)


@router.get("/search")
async def query(query: str):
    with db.get_dbs() as dbs:
        search_indexer = search_src.SearchIndexer(dbs=dbs)
        result = search_indexer.search(query)
        return result
