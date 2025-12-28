from sqlalchemy.orm import Session
from models.user_model import User, UserRole
from repositories.user_repo import UserRepository
from schemas.auth_schema import RegisterRequest, LoginRequest
from utils.password_utils import get_password_hash, verify_password
from utils.jwt_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.exceptions import AuthError, ValidationError

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, request: RegisterRequest) -> User:
        if request.role not in [UserRole.AUTHOR, UserRole.READER]:
            raise ValidationError("Registration allowed only for author or reader.")
        
        existing_user = self.user_repo.get_by_username(request.username)
        if existing_user:
            raise ValidationError("Username already exists.")

        hashed_password = get_password_hash(request.password)
        new_user = User(
            username=request.username,
            password_hash=hashed_password,
            role=request.role
        )
        return self.user_repo.create_user(new_user)

    def login(self, request: LoginRequest) -> dict:
        user = self.user_repo.get_by_username(request.username)
        if not user or not verify_password(request.password, user.password_hash):
            raise AuthError("Invalid username or password")

        if not user.is_active:
            raise AuthError("User is inactive")

        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username, "role": user.role.value}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
