import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import api.models.page_word as page_word_mdl
import core.exeptions.exception as exceptions


class PageWordCrud:
    @classmethod
    def create(
        cls,
        db: sa_orm.Session,
        page_id: int,
        word_id: int,
        occurence: int,
        frequency: float,
    ) -> page_word_mdl.PageWord:
        existing_page_word = (
            db.query(page_word_mdl.PageWord)
            .filter(page_word_mdl.PageWord.page_id == page_id)
            .filter(page_word_mdl.PageWord.word_id == word_id)
            .first()
        )
        if existing_page_word:
            existing_page_word.occurence = occurence
            existing_page_word.frequency = frequency
            db.flush()
            db.refresh(existing_page_word)
            return existing_page_word
        page_word = page_word_mdl.PageWord(
            page_id=page_id, word_id=word_id, occurence=occurence, frequency=frequency
        )
        db.add(page_word)
        db.flush()
        db.refresh(page_word)
        return page_word
