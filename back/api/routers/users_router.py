import fastapi

import api.schemas.auth_schemas as auth_sch
import api.services.user_services as user_srv
import db.sessions as db

router = fastapi.APIRouter()


@router.post("/users/signup")
async def signup(
    user: auth_sch.Signup,
    dbs=fastapi.Depends(db.get_dbs),
):
    user_service = user_srv.UserService(dbs=dbs)
    result = user_service.signup(user)

    return result


@router.post("/users/login")
def login(
    user: auth_sch.Login,
    dbs=fastapi.Depends(db.get_dbs),
):
    user_service = user_srv.UserService(dbs=dbs)
    return user_service.login(email=user.email)
