import sqlalchemy as sa
import back.api.models.word as word_mdl
import core.exeptions.exception as exceptions


class wordCrud:
    @classmethod
    def create(cls, db: sa.orm.Session, word: word_mdl.word) -> word_mdl.word:
        try:
            db.add(word)
            db.commit()
            db.refresh(word)
            return word
        except Exception:
            db.rollback()
            raise exceptions.InternalServerError()
