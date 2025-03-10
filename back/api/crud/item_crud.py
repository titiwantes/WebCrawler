import sqlalchemy as sa
import api.models.item as item_mdl
import core.exeptions.exception as exceptions


class ItemCrud:
    @classmethod
    def get_item_by_id(cls, db: sa.orm.Session, item_id: int) -> item_mdl.Item:
        try:
            item = db.query(item_mdl.Item).filter(item_mdl.Item.id == item_id).first()
            return item
        except Exception:
            raise exceptions.InternalServerError()

    @classmethod
    def create(cls, db: sa.orm.Session, item: item_mdl.Item) -> item_mdl.Item:
        try:
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        except Exception:
            db.rollback()
            raise exceptions.InternalServerError()
