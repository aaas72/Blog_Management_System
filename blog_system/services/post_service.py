from sqlalchemy.orm import Session
from models.post_model import Post, PostStatus
from models.user_model import User, UserRole
from repositories.post_repo import PostRepository
from services.audit_service import AuditService
from schemas.post_schema import PostCreate, PostUpdate
from utils.exceptions import NotFoundError, ForbiddenError, ValidationError

class PostService:
    def __init__(self, db: Session):
        self.post_repo = PostRepository(db)
        self.audit_service = AuditService(db)

    def _check_ownership(self, user: User, post: Post):
        if user.role == UserRole.ADMIN:
            return
        if user.role == UserRole.AUTHOR:
            if post.author_id != user.id:
                raise ForbiddenError("You can only manage your own posts")
        else:
            raise ForbiddenError("Permission denied")

    def create_post(self, user: User, post_data: PostCreate) -> Post:
        if user.role not in [UserRole.ADMIN, UserRole.AUTHOR]:
            raise ForbiddenError("Only admins and authors can create posts")
        
        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            author_id=user.id,
            status=PostStatus.DRAFT
        )
        created_post = self.post_repo.create_post(new_post)
        
        # Log Audit
        self.audit_service.log_action(
            user_id=user.id,
            action="CREATE",
            entity_type="Post",
            entity_id=created_post.id,
            details={"title": created_post.title}
        )
        
        return created_post

    def get_post(self, post_id: int) -> Post:
        post = self.post_repo.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("Post not found")
        return post

    def update_post(self, user: User, post_id: int, post_data: PostUpdate) -> Post:
        post = self.get_post(post_id)
        self._check_ownership(user, post)

        if post.status == PostStatus.PUBLISHED:
            raise ValidationError("Cannot update a published post. Archive it or restore to draft first.")
        
        if post.status == PostStatus.ARCHIVED:
             raise ValidationError("Cannot update an archived post.")

        changes = {}
        if post_data.title:
            changes["old_title"] = post.title
            post.title = post_data.title
            changes["new_title"] = post.title
        if post_data.content:
            post.content = post_data.content
            changes["content_updated"] = True
            
        updated_post = self.post_repo.update_post(post)

        if changes:
            self.audit_service.log_action(
                user_id=user.id,
                action="UPDATE",
                entity_type="Post",
                entity_id=updated_post.id,
                details=changes
            )

        return updated_post

    def publish_post(self, user: User, post_id: int) -> Post:
        post = self.get_post(post_id)
        if user.role not in [UserRole.ADMIN, UserRole.AUTHOR]:
            raise ForbiddenError("Permission denied")
        self._check_ownership(user, post)

        if post.status != PostStatus.DRAFT:
            raise ValidationError(f"Cannot publish post from status '{post.status}'. Must be draft.")
        
        # Business Rule: Content length check
        if len(post.content) < 20: # Example rule
            raise ValidationError("Content too short to publish (min 20 chars).")

        post.status = PostStatus.PUBLISHED
        updated_post = self.post_repo.update_post(post)

        self.audit_service.log_action(
            user_id=user.id,
            action="PUBLISH",
            entity_type="Post",
            entity_id=updated_post.id
        )

        return updated_post

    def archive_post(self, user: User, post_id: int) -> Post:
        post = self.get_post(post_id)
        self._check_ownership(user, post)

        if post.status != PostStatus.PUBLISHED:
            raise ValidationError("Only published posts can be archived.")

        post.status = PostStatus.ARCHIVED
        updated_post = self.post_repo.update_post(post)

        self.audit_service.log_action(
            user_id=user.id,
            action="ARCHIVE",
            entity_type="Post",
            entity_id=updated_post.id
        )

        return updated_post

    def restore_post(self, user: User, post_id: int) -> Post:
        post = self.get_post(post_id)
        self._check_ownership(user, post)

        if post.status != PostStatus.ARCHIVED:
            raise ValidationError("Only archived posts can be restored.")

        post.status = PostStatus.DRAFT
        updated_post = self.post_repo.update_post(post)

        self.audit_service.log_action(
            user_id=user.id,
            action="RESTORE",
            entity_type="Post",
            entity_id=updated_post.id
        )

        return updated_post

    def delete_post(self, user: User, post_id: int):
        post = self.get_post(post_id)
        self._check_ownership(user, post)

        if post.status == PostStatus.ARCHIVED:
            raise ValidationError("Cannot delete archived posts. Restore them first.")

        self.post_repo.delete_post(post)

        self.audit_service.log_action(
            user_id=user.id,
            action="DELETE",
            entity_type="Post",
            entity_id=post_id
        )

    def list_posts(self, user: User = None, only_mine: bool = False):
        if only_mine:
            if not user:
                raise ForbiddenError("Authentication required")
            return self.post_repo.list_posts(author_id=user.id)
        else:
            return self.post_repo.list_posts(status=PostStatus.PUBLISHED)
