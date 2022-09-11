from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from routers.setting import get_db, authenticate_user, \
    create_access_token, token_expires, token_excetin

router = APIRouter(
    tags=['authentication']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(),
              db: Session = Depends(get_db)):
    user = authenticate_user(request.username, request.password, db)
    if not user:
        raise token_excetin()
    access_token = create_access_token(user,
                                       expires_delta=token_expires)
    return {
        'token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'user_name': user.username
    }
