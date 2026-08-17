from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRETY_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone



auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id_user, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    date_expiration = datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": str(id_user), "exp":date_expiration}
    jwt_codification = jwt.encode(dic_info,SECRETY_KEY, ALGORITHM)
    return jwt_codification

def user_autentication(email, passord, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(passord, user.password):
        return False
    return user


@auth_router.get("/")
async def autentication(session=Depends(get_session)):
    
    users = session.query(User).all()

    return [users]

@auth_router.post("/create_account")
async def create_account( user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already registred")
    else:
        password_crypt = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, password_crypt, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"message":"User succesfully registred"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = user_autentication(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credencials")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration_token=timedelta(days=7)) 
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
            }
    
    
@auth_router.post("/login-form")
async def login_form(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = user_autentication(data_form.username, data_form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid credencials")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }







































   