import sqlalchemy as sa
import sqlalchemy.orm as orm
import api.models.page as page_mdl
import core.exeptions.exception as exceptions


class PageCrud:

    @classmethod
    def create(cls, db: orm.Session, page: page_mdl.Page) -> page_mdl.Page:
        existing_page = (
            db.query(page_mdl.Page).filter(page_mdl.Page.url == page.url).first()
        )
        if existing_page:
            existing_page.title = page.title
            existing_page.content = page.content
            return existing_page

        db.add(page)
        db.flush()
        db.refresh(page)
        return page

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

    @classmethod
    def get_all_urls(cls, db: sa.orm.Session) -> list[str]:
        try:
            result = db.query(page_mdl.Page.url).all()
            return [url for url, in result]
        except Exception as e:
            raise exceptions.InternalServerError(e)
