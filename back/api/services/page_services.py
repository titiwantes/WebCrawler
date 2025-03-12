import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import api.crud.page_crud as page_crud
import api.models.page as page_mdl
import api.crud.page_crud as page_crud
import api.models.link as link_mdl
import api.crud.link_crud as link_crud
import api.schemas.page_schemas as page_sch
import db.sessions as sessions


class PageService:
    def __init__(self, dbs: tuple[sa_orm.Session, sa_orm.Session]):
        self.reader, self.writer = dbs

    def create_page(self, page_data: page_sch.CreatePage) -> page_mdl.Page:
        new_page = page_mdl.Page(**page_data.dict())
        return page_crud.PageCrud.create(self.writer, new_page)

    def add_link(self, link: link_mdl.Link, page_id: int) -> None:
        link.from_page_id = page_id
        link_crud.LinkCrud.create(self.writer, link)

    def add_links(self, links: list[link_mdl.Link], page_id: int) -> None:
        for link in links:
            link.from_page_id = page_id
            page_crud.LinkCrud.create(self.writer, link)

    def create_from_scrapping(self, url: str, title: str, content: str) -> None:
        # words = {word.lower().strip() for word in content.split()} if content else {}

        with sessions.get_db_writer() as transaction_db:
            page = page_mdl.Page(url=url, title=title, content=content)
            page = page_crud.PageCrud.create(transaction_db, page)
            transaction_db.commit()
            transaction_db.refresh(page)
            print(f"{page.id} : {page.url}")
