import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import api.crud.page_crud as page_crud
import api.models.page as page_mdl
import api.crud.page_crud as page_crud
import api.models.link as link_mdl
import api.crud.link_crud as link_crud
import api.schemas.page_schemas as page_sch
import api.crud.word_crud as word_crud
import api.crud.page_word_crud as page_word_crud
import db.sessions as sessions
import re


class PageService:
    def __init__(self, dbs: tuple[sa_orm.Session, sa_orm.Session]):
        self.reader, self.writer = dbs

    @classmethod
    def words_from_text(cls, text: str) -> set[str]:
        return {word.lower() for word in re.findall(r"\b\w+\b", text)}

    def create_page(self, page_data: page_sch.CreatePage) -> page_mdl.Page:
        new_page = page_mdl.Page(**page_data.dict())
        return page_crud.PageCrud.create(self.writer, new_page)

    def add_link(self, link: str, page_id: int) -> None:
        link.from_page_id = page_id
        link_crud.LinkCrud.create(self.writer, link)

    def add_links(self, links: list[link_mdl.Link], page_id: int) -> None:
        for link in links:
            link.from_page_id = page_id
            page_crud.LinkCrud.create(self.writer, link)

    def create_from_scrapping(self, url: str, title: str, content: str) -> int:
        words = self.words_from_text(content)
        with sessions.get_db_writer() as transaction_db:
            page = page_mdl.Page(url=url, title=title, content=content)

            page = page_crud.PageCrud.create(transaction_db, page)
            for word in words:
                word = word_crud.wordCrud.create(transaction_db, word)
                page_word_crud.PageWordCrud.create(transaction_db, page.id, word.id)

            page_id = page.id
            transaction_db.commit()
            return page_id
