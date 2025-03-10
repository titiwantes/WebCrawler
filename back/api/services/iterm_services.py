import sqlalchemy as sa
import api.schemas.item_schemas as item_sch
import api.models.item as item_mdl
import api.crud.item_crud as item_crud
import core.exeptions.exception as exceptions


class ItemService:
    def __init__(self, dbs: tuple[sa.orm.Session, sa.orm.Session]):
        self.reader, self.writer = dbs

    def create_item(self, item: item_sch.ItemCreate) -> item_mdl.Item:
        new_item = item_mdl.Item(name=item.name, description=item.description)
        item_crud.ItemCrud.create(self.writer, new_item)

    def get_item_by_id(self, item_id: int) -> item_mdl.Item:
        item = item_crud.ItemCrud.get_item_by_id(self.reader, item_id)
        if not item:
            raise exceptions.NotFound
        return item
