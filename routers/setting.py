from fastapi import HTTPException, Depends, HTTPException, status
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import models, pprint

# db
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def http_exception():
    return HTTPException(status_code=404, detail="not found")


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def model_exception(models):
    if models is None:
        raise http_exception()

# token
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

SECRET_KEY = "762df4a48e196b16508658c1d926b22a66309ebd966cad147b016be9bffd662"
ALGOROTHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
token_expires = timedelta(hours=5)

def get_password_hash(password):
    get_password = bcrypt_context.hash(password)
    return get_password


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users) \
        .filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


def create_access_token(user,
                        expires_delta: Optional[timedelta] = None):
    encode = {'sub': user.username, 'id': user.id}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # minutes days hours
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp': expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGOROTHM)


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


def token_excetin():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response


async def get_current_user(token:str = Depends(oauth2_bearer),
                           db:Session= Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGOROTHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, 'id': user_id}
    except JWTError:
        raise get_user_exception()

    user = db.query(DbUser).filter(DbUser.username == username).first()
    return user
