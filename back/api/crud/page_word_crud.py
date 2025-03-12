import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import api.models.page_word as page_word_mdl
import core.exeptions.exception as exceptions


class PageWordCrud:
    @classmethod
    def create(
        cls, db: sa_orm.Session, page_word: page_word_mdl.PageWord
    ) -> page_word_mdl.PageWord:
        try:
            db.add(page_word)
            db.commit()
            db.refresh(page_word)
            return page_word
        except Exception:
            db.rollback()
            raise exceptions.InternalServerError()
