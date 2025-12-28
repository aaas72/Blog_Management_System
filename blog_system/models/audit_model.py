from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database.db import Base
from sqlalchemy.orm import relationship

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, etc.
    entity_type = Column(String(50), nullable=False) # Post, User, etc.
    entity_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for system actions or if user deleted? Better keep it linked.
    details = Column(Text, nullable=True) # JSON or simple text
    timestamp = Column(TIMESTAMP, server_default=func.now())

    user = relationship("models.user_model.User")
