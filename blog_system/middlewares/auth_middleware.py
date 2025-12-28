from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.db import get_db
from repositories.user_repo import UserRepository
from utils.jwt_utils import decode_access_token
from utils.exceptions import AuthError, ForbiddenError
from models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

from jose import ExpiredSignatureError

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        raise AuthError("Token has expired", 401)
        
    if not payload:
        raise AuthError("Invalid authentication credentials", 401)
    
    username: str = payload.get("username")
    if username is None:
        raise AuthError("Invalid authentication credentials", 401)
        
    repo = UserRepository(db)
    user = repo.get_by_username(username)
    if user is None:
        raise AuthError("User not found", 401)
        
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise ForbiddenError("Operation not permitted")
        return user
