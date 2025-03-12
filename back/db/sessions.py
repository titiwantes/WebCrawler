import enum
import typing

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import core.settings
import contextlib

settings = core.settings.settings


class SessionType(enum.Enum):
    WRITER = "writer"
    READER = "reader"


_engine = None


def get_engine(db_url: str = settings.DB_URL) -> sa.engine.base.Engine:
    global _engine
    if _engine is not None:
        return _engine
    return sa.create_engine(db_url)


def create_session(
    *,
    session_type: SessionType,
    db_url: str = settings.DB_URL,
    autocommit: bool = False,
    autoflush: bool = True
) -> sa_orm.sessionmaker:
    return sa_orm.sessionmaker(
        bind=get_engine(db_url=db_url),
        autoflush=autoflush,
        autocommit=autocommit,
        info={"type": session_type.value},
    )


@contextlib.contextmanager
def get_db_writer(
    *, autocommit: bool = False, autoflush: bool = True, db_url: str = settings.DB_URL
) -> typing.Generator[sa_orm.Session, None, None]:
    db = create_session(
        session_type=SessionType.WRITER,
        autocommit=autocommit,
        autoflush=autoflush,
        db_url=db_url,
    )()
    try:
        yield db
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def get_db_reader(
    *, autocommit: bool = False, autoflush: bool = True, db_url: str = settings.DB_URL
) -> typing.Generator[sa_orm.Session, None, None]:
    db = create_session(
        session_type=SessionType.READER,
        autocommit=autocommit,
        autoflush=autoflush,
        db_url=db_url,
    )()
    try:
        yield db
    finally:
        db.close()


@contextlib.contextmanager
def get_dbs(
    *,
    db_url: str = settings.DB_URL,
    reader_autocommit: bool = False,
    reader_autoflush: bool = True,
    writer_autocommit: bool = False,
    writer_autoflush: bool = True
) -> typing.Generator[tuple[sa_orm.Session, sa_orm.Session], None, None]:
    reader = create_session(
        session_type=SessionType.READER,
        autocommit=reader_autocommit,
        autoflush=reader_autoflush,
        db_url=db_url,
    )()
    writer = create_session(
        session_type=SessionType.WRITER,
        autocommit=writer_autocommit,
        autoflush=writer_autoflush,
        db_url=db_url,
    )()
    try:
        yield reader, writer
        writer.commit()

    except Exception as e:
        writer.rollback()
        raise e

    finally:
        reader.close()
        writer.close()
