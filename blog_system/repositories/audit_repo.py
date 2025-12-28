from sqlalchemy.orm import Session
from models.audit_model import AuditLog

class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, log: AuditLog) -> AuditLog:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
