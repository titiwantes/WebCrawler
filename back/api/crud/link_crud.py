import sqlalchemy as sa
import api.models.link as link_mdl
import core.exeptions.exception as exceptions


class LinkCrud:
    @classmethod
    def create(cls, db: sa.orm.Session, link: link_mdl.Link) -> link_mdl.Link:
        try:
            db.add(link)
            db.commit()
            db.refresh(link)
            return link
        except Exception:
            db.rollback()
            raise exceptions.InternalServerError()
