from sqlalchemy.orm import Session
from models.post_model import Post, PostStatus
from typing import List, Optional

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def update_post(self, post: Post) -> Post:
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post: Post):
        self.db.delete(post)
        self.db.commit()

    def list_posts(self, status: Optional[PostStatus] = None, author_id: Optional[int] = None) -> List[Post]:
        query = self.db.query(Post)
        if status:
            query = query.filter(Post.status == status)
        if author_id:
            query = query.filter(Post.author_id == author_id)
        return query.all()
