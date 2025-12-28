from fastapi import APIRouter, Depends, Request, status, Path
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from services.post_service import PostService
from schemas.post_schema import PostCreate, PostUpdate, PostResponse
from utils.responses import standard_response
from middlewares.auth_middleware import get_current_user, RoleChecker
from models.user_model import User, UserRole

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("")
def create_post(
    request: Request, 
    data: PostCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    post = service.create_post(user, data)
    post_data = PostResponse.model_validate(post).model_dump()
    return standard_response(
        success=True,
        data=post_data,
        message="Post created successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.get("/mine")
def list_my_posts(
    request: Request, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    posts = service.list_posts(user, only_mine=True)
    posts_data = [PostResponse.model_validate(p).model_dump() for p in posts]
    return standard_response(
        success=True,
        data=posts_data,
        request_id=getattr(request.state, "request_id", None)
    )

@router.get("/{post_id}")
def get_post(
    request: Request, 
    post_id: int, 
    db: Session = Depends(get_db)
):
    service = PostService(db)
    post = service.get_post(post_id)
    post_data = PostResponse.model_validate(post).model_dump()
    return standard_response(
        success=True,
        data=post_data,
        request_id=getattr(request.state, "request_id", None)
    )

@router.put("/{post_id}")
def update_post(
    request: Request, 
    post_id: int, 
    data: PostUpdate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    post = service.update_post(user, post_id, data)
    post_data = PostResponse.model_validate(post).model_dump()
    return standard_response(
        success=True,
        data=post_data,
        message="Post updated successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.post("/{post_id}/publish")
def publish_post(
    request: Request, 
    post_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    post = service.publish_post(user, post_id)
    post_data = PostResponse.model_validate(post).model_dump()
    return standard_response(
        success=True,
        data=post_data,
        message="Post published successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.post("/{post_id}/archive")
def archive_post(
    request: Request, 
    post_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    post = service.archive_post(user, post_id)
    post_data = PostResponse.model_validate(post).model_dump()
    return standard_response(
        success=True,
        data=post_data,
        message="Post archived successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.post("/{post_id}/restore")
def restore_post(
    request: Request, 
    post_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    post = service.restore_post(user, post_id)
    post_data = PostResponse.model_validate(post).model_dump()
    return standard_response(
        success=True,
        data=post_data,
        message="Post restored to draft successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.delete("/{post_id}")
def delete_post(
    request: Request, 
    post_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    service = PostService(db)
    service.delete_post(user, post_id)
    return standard_response(
        success=True,
        message="Post deleted successfully",
        request_id=getattr(request.state, "request_id", None)
    )

@router.get("")
def list_posts(
    request: Request, 
    db: Session = Depends(get_db)
):
    service = PostService(db)
    posts = service.list_posts(only_mine=False)
    posts_data = [PostResponse.model_validate(p).model_dump() for p in posts]
    return standard_response(
        success=True,
        data=posts_data,
        request_id=getattr(request.state, "request_id", None)
    )
