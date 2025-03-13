import sqlalchemy as sa
import sqlalchemy.orm as orm
import api.models.page as page_mdl
import api.models.page as page_mdl
import api.models.page_word as page_word_mdl
import api.models.word as word_mdl
import math


class SearchIndexer:
    def __init__(self, dbs: tuple[orm.Session, orm.Session]):
        self.reader, self.writer = dbs

    def count_pages(self) -> int:
        stmt = sa.select(sa.func.count(page_mdl.Page.id))
        return self.reader.execute(stmt).scalar()

    def count_pages_with_word(self, word: str) -> int:
        stmt = (
            sa.select(sa.func.count(sa.func.distinct(page_mdl.Page.id)))
            .join(
                page_word_mdl.PageWord,
                page_mdl.Page.id == page_word_mdl.PageWord.page_id,
            )
            .join(word_mdl.Word, page_word_mdl.PageWord.word_id == word_mdl.Word.id)
            .where(word_mdl.Word.word == word)
        )
        return self.reader.execute(stmt).scalar()

    def get_term_frequency(self, word: str):
        stmt = (
            sa.select(page_word_mdl.PageWord.frequency, page_mdl.Page.url)
            .join(page_mdl.Page, page_mdl.Page.id == page_word_mdl.PageWord.page_id)
            .join(word_mdl.Word, page_word_mdl.PageWord.word_id == word_mdl.Word.id)
            .where(word_mdl.Word.word == word)
            .order_by(sa.desc(page_word_mdl.PageWord.frequency))
        )
        return self.reader.execute(stmt).all()

    def search(self, req: str) -> list[str]:
        urls = {}

        total_pages = self.count_pages()

        for word in req.split():
            pages_with_word = self.count_pages_with_word(word=word)

            if pages_with_word == 0:
                continue

            inverse_document_frequency = math.log(total_pages / pages_with_word)
            term_frequency = self.get_term_frequency(word=word)

            for term_frequency, url in term_frequency:
                tf_idf = term_frequency * inverse_document_frequency
                urls[url] = urls.get(url, 0) + tf_idf

        sorted_urls = sorted(urls.keys(), key=lambda x: x[1], reverse=True)
        return sorted_urls
