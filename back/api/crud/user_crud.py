import sqlalchemy as sa

import api.models.user as user_mdls
import api.models.user_auth_data as uad
import api.schemas.user_schemas as user_sch
import core.exeptions.exception as exceptions


class UserCrud:
    @classmethod
    def get_user_by_email(cls, db: sa.orm.Session, email: str) -> user_mdls.User:
        try:
            user = (
                db.query(user_mdls.User)
                .join(uad.UserAuthData)
                .filter(uad.UserAuthData.email == email)
                .first()
            )
            return user
        except Exception:
            raise exceptions.InternalServerError()

    @classmethod
    def create(cls, db: sa.orm.Session, user: user_sch.UserCreate) -> user_mdls.User:
        try:
            user = user_mdls.User(**user.model_dump())
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception:
            raise exceptions.InternalServerError()

    @classmethod
    def get_user_auth_data_by_email(cls, db: sa.orm.Session, email: str):
        try:
            user_auth_data = (
                db.query(uad.UserAuthData)
                .filter(uad.UserAuthData.email == email)
                .first()
            )
            return user_auth_data

        except Exception:
            raise exceptions.InternalServerError()
