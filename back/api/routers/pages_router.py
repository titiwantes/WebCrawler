import fastapi
import db.sessions as db
import api.services.page_services as page_srv
import api.schemas.page_schemas as page_sch
import core.celery as celery_app

router = fastapi.APIRouter()


@router.post("/pages/create")
async def create(page: page_sch.CreatePage, dbs=fastapi.Depends(db.get_dbs)):
    result = celery_app.crawl.delay(page.url)
    print("result = ", result)
    page_service = page_srv.PageService(dbs=dbs)
    page_service.create_page(page)
    return page
