import sqlalchemy as sa
import api.models.word as word_mdl
import core.exeptions.exception as exceptions
import sqlalchemy.dialects.mysql as mysql


class wordCrud:
    @classmethod
    def create(cls, db: sa.orm.Session, word: str) -> word_mdl.Word:
        existing_word = (
            db.query(word_mdl.Word).filter(word_mdl.Word.word == word).first()
        )
        if existing_word:
            return existing_word
        word = word_mdl.Word(word=word)
        db.add(word)
        db.flush()
        db.refresh(word)
        return word

    @classmethod
    def create_many(cls, db: sa.orm.Session, words: set[str]) -> list[word_mdl.Word]:
        insert_stmt = mysql.insert(word_mdl.Word).values(
            [{"word": word} for word in words]
        )
        upsert_stmt = insert_stmt.on_duplicate_key_update(
            word=insert_stmt.inserted.word
        )
        db.execute(upsert_stmt)
        return db.query(word_mdl.Word).filter(word_mdl.Word.word.in_(words)).all()
