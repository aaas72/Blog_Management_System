from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.db import get_db
from services.auth_service import AuthService
from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from utils.responses import standard_response
from middlewares.auth_middleware import get_current_user
from models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(request: Request, data: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.register(data)
    # Convert to schema manually or let Pydantic handle it if we return schema
    # But we want standard_response wrapper
    user_data = UserResponse.model_validate(user).model_dump()
    return standard_response(
        success=True,
        data=user_data,
        message="User registered successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.post("/login")
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token_data = service.login(data)
    return standard_response(
        success=True,
        data=token_data,
        message="Login successful",
        request_id=getattr(request.state, "request_id", None)
    )

@router.get("/me")
def get_me(request: Request, user: User = Depends(get_current_user)):
    user_data = UserResponse.model_validate(user).model_dump()
    return standard_response(
        success=True,
        data=user_data,
        request_id=getattr(request.state, "request_id", None)
    )
