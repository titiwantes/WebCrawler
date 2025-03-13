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
    def words_from_text(cls, text: str) -> list[str]:
        return [word.lower() for word in re.findall(r"\b\w+\b", text)]

    def words_occurrences_from_words(self, words: list[str]) -> dict[str, int]:
        words_occurrences = {}
        for word in words:
            if word in words_occurrences:
                words_occurrences[word] += 1
            else:
                words_occurrences[word] = 1
        return words_occurrences

    def create_page(self, page_data: page_sch.CreatePage) -> page_mdl.Page:
        new_page = page_mdl.Page(**page_data.dict())
        return page_crud.PageCrud.create(self.writer, new_page)

    def add_link(self, from_page_id: str, to_page_id: int) -> None:
        link = link_mdl.Link(from_page_id=from_page_id, to_page_id=to_page_id)
        print(f"Link from: {from_page_id} to: {to_page_id}")
        with sessions.get_db_writer() as transaction_db:
            link_crud.LinkCrud.create(transaction_db, link)

    def add_links(self, links: list[link_mdl.Link], page_id: int) -> None:
        for link in links:
            link.from_page_id = page_id
            page_crud.LinkCrud.create(self.writer, link)

    def add_incoming_link(self, page_url: str) -> None:
        with sessions.get_db_writer() as transaction_db:
            stmt = sa.text(
                """
                UPDATE pages
                SET incoming_links = incoming_links + 1
                WHERE url = :url
                """
            ).bindparams(url=page_url)
            transaction_db.execute(stmt)
            transaction_db.commit()

    def create_from_scrapping(self, url: str, title: str, content: str) -> int:
        words = self.words_from_text(content)
        words_count = len(words)
        page_id = None
        with sessions.get_db_writer() as transaction_db:
            page = page_mdl.Page(
                url=url, title=title, content=content, words_count=words_count
            )
            page = page_crud.PageCrud.create(transaction_db, page)

            words_occurrences = self.words_occurrences_from_words(words)

            for word in words_occurrences.keys():
                word_obj = word_crud.wordCrud.create(transaction_db, word)
                page_word_crud.PageWordCrud.create(
                    db=transaction_db,
                    page_id=page.id,
                    word_id=word_obj.id,
                    occurence=words_occurrences[word],
                    frequency=words_occurrences[word] / words_count,
                )

            print(f"url: {page.url} | id: {page.id} | words: {len(words)}")
            page_id = page.id
            transaction_db.commit()
        return page_id
