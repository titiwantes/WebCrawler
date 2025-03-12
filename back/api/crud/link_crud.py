import sqlalchemy as sa
import api.models.link as link_mdl
import core.exeptions.exception as exceptions


class LinkCrud:
    @classmethod
    def create(cls, db: sa.orm.Session, link: link_mdl.Link) -> link_mdl.Link:
        existing_link = (
            db.query(link_mdl.Link)
            .filter(link_mdl.Link.from_page_id == link.from_page_id)
            .filter(link_mdl.Link.to_page_id == link.to_page_id)
            .first()
        )
        if existing_link:
            return existing_link
        db.add(link)
        db.flush()
        db.refresh(link)
        return link
