import sqlalchemy as sa

import api.crud.user_auth_data_crud as uad_crud
import api.crud.user_crud as user_crud
import api.schemas.auth_schemas as auth_sch
import api.schemas.user_auth_data_schemas as uad_sch
import api.schemas.user_schemas as user_sch
import api.utils.security as security
import core.exeptions.exception as exeptions


class UserService:
    def __init__(self, dbs: tuple[sa.orm.Session, sa.orm.Session]):
        self.reader, self.writer = dbs

    def signup(self, auth: auth_sch.Signup):
        existing_user = user_crud.UserCrud.get_user_by_email(
            db=self.reader, email=auth.email
        )
        if existing_user:
            raise exeptions.NotFound("Email already registered")

        password_hash = security.hash_password(auth.password)

        user = user_crud.UserCrud.create(
            self.writer,
            user_sch.UserCreate(),
        )

        user_auth_data = uad_crud.UserAuthDataCrud.create(
            self.writer,
            uad_sch.UserAuthDataCreate(
                email=auth.email,
                password_hash=password_hash,
                user_id=user.id,
                name=auth.name,
            ),
        )

        return user_sch.UserCreateOut(
            name=user_auth_data.name,
            email=user_auth_data.email,
            id=user.id,
        )

    def login(self, email: str) -> auth_sch.LoginOut:
        try:
            user_auth_data = user_crud.UserCrud.get_user_auth_data_by_email(
                email=email, db=self.reader
            )
            if not user_auth_data:
                raise exeptions.NotFound("User not found")

            user = user_crud.UserCrud.get_user_by_email(db=self.reader, email=email)

            return auth_sch.LoginOut(email=email, id=user.id, name=user_auth_data.name)
        except:
            raise exeptions.InternalServerError()
