import fastapi

import api.schemas.item_schemas as item_sch
import api.services.iterm_services as item_srv
import api.crud.item_crud as item_crud
import db.sessions as db

router = fastapi.APIRouter()


@router.post("/items/create")
async def create_item(
    item: item_sch.ItemCreate,
    dbs=fastapi.Depends(db.get_dbs),
):
    item_service = item_srv.ItemService(dbs=dbs)
    item_service.create_item(item)
    return item


@router.get("/items/{item_id}")
async def get_item(
    item_id: int,
    dbs=fastapi.Depends(db.get_dbs),
):
    item_service = item_srv.ItemService(dbs=dbs)
    item = item_service.get_item_by_id(item_id)
    return item
