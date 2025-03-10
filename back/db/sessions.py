import enum
import typing

import sqlalchemy as sa

import core.settings

settings = core.settings.settings


class SessionType(enum.Enum):
    WRITER = "writer"
    READER = "reader"


_engine = None


def get_engine() -> sa.engine.base.Engine:
    global _engine
    if _engine is not None:
        return _engine
    return sa.create_engine(settings.DB_URL)


def create_session(
    *, session_type: SessionType, autocommit: bool = False, autoflush: bool = True
) -> sa.orm.sessionmaker:
    return sa.orm.sessionmaker(
        bind=get_engine(),
        autoflush=autoflush,
        autocommit=autocommit,
        info={"type": session_type.value},
    )


def get_db_writer(
    *, autocommit: bool = False, autoflush: bool = True
) -> typing.Generator[sa.orm.Session, None, None]:
    db = create_session(
        session_type=SessionType.WRITER, autocommit=autocommit, autoflush=autoflush
    )()
    try:
        yield db
    finally:
        db.close()


def get_db_reader(
    *, autocommit: bool = False, autoflush: bool = True
) -> typing.Generator[sa.orm.Session, None, None]:
    db = create_session(
        session_type=SessionType.READER, autocommit=autocommit, autoflush=autoflush
    )()
    try:
        yield db
    finally:
        db.close()


def get_dbs(
    *,
    reader_autocommit: bool = False,
    reader_autoflush: bool = True,
    writer_autocommit: bool = False,
    writer_autoflush: bool = True
) -> typing.Generator[tuple[sa.orm.Session, sa.orm.Session], None, None]:
    reader = create_session(
        session_type=SessionType.READER,
        autocommit=reader_autocommit,
        autoflush=reader_autoflush,
    )()
    writer = create_session(
        session_type=SessionType.WRITER,
        autocommit=writer_autocommit,
        autoflush=writer_autoflush,
    )()
    try:
        yield reader, writer
    finally:
        reader.close()
        writer.close()
