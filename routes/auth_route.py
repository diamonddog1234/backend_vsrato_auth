from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, Response, Cookie
from depends.get_db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models.user import User
from db.models.session import Session as UserSession
from schema.register_schema import RegisterSchema
from schema.success_auth import SuccessAuth
from schema.login_schema import LoginSchema
from typing import Annotated
from uuid import UUID

auth_router = APIRouter(tags=["users"])

@auth_router.post("/register")
async def register(register_schema: RegisterSchema,  session: Session = Depends(get_db)):
    repeat_user_query = select(User).where(User.name == register_schema.login)
    repeat_user = session.execute(repeat_user_query).scalar_one_or_none()
    if repeat_user != None:
        raise HTTPException(409)
    user = User()
    user.name = register_schema.login
    user.password_hash = register_schema.password
    session.add(user)
    session.commit()
    return 

    

@auth_router.post("/login")
async def login(login_schema: LoginSchema, response: Response,  session: Session = Depends(get_db)) -> SuccessAuth:
    login_user_query = select(User)\
        .where(User.name == login_schema.login)\
            .where(User.password_hash == login_schema.password)
    login_user = session.execute(login_user_query).scalar_one_or_none()
    if login_user == None:
        raise HTTPException(400)
    else:
        user_session = UserSession()
        user_session.user_id = login_user.id
        session.add(user_session)
        session.commit()
        response.set_cookie("session_id", user_session.id)
        return SuccessAuth(
            id = login_user.id,
            login=login_user.name
        )

@auth_router.put("/check_me")
async def check_me(session: Session = Depends(get_db), session_id: Annotated[UUID | None, Cookie()] = None):
    login_session_query = select(UserSession).where(UserSession.id == session_id)
    login_session: UserSession | None = session.execute(login_session_query).scalar_one_or_none()
    return login_session.user.name
