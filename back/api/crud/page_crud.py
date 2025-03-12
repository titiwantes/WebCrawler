import sqlalchemy as sa
import api.models.page as page_mdl
import core.exeptions.exception as exceptions


class PageCrud:
    @classmethod
    def create(cls, db: sa.orm.Session, page: page_mdl.Page) -> page_mdl.Page:
        try:
            existing_page = (
                db.query(page_mdl.Page).filter(page_mdl.Page.url == page.url).first()
            )
            if existing_page:
                existing_page.title = page.title
                existing_page.content = page.content
                db.commit()
                db.refresh(existing_page)
                return existing_page
            db.add(page)
            db.commit()
            db.refresh(page)
            return page
        except Exception as e:
            db.rollback()
            raise exceptions.InternalServerError(e)

    @classmethod
    def get_by_url(cls, db: sa.orm.Session, url: str) -> page_mdl.Page:
        try:
            return db.query(page_mdl.Page).filter(page_mdl.Page.url == url).first()
        except Exception as e:
            raise exceptions.InternalServerError(e)

    @classmethod
    def get_by_id(cls, db: sa.orm.Session, page_id: int) -> page_mdl.Page:
        try:
            return db.query(page_mdl.Page).filter(page_mdl.Page.id == page_id).first()
        except Exception as e:
            raise exceptions.InternalServerError(e)
