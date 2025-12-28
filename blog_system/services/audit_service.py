from sqlalchemy.orm import Session
from repositories.audit_repo import AuditRepository
from models.audit_model import AuditLog
from typing import Optional
import json

class AuditService:
    def __init__(self, db: Session):
        self.audit_repo = AuditRepository(db)

    def log_action(self, user_id: int, action: str, entity_type: str, entity_id: int, details: Optional[dict] = None):
        """
        Logs an action performed by a user on an entity.
        """
        details_str = json.dumps(details) if details else None
        
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details_str
        )
        return self.audit_repo.create_log(log)
