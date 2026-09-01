from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("recovery_cases.id"))
    decision_id = Column(String, unique=True)
    agent = Column(String)
    action = Column(String)
    reason = Column(String)
    evidence = Column(JSONB)
    policy_checks = Column(JSONB)
    execution_result = Column(String)
    outcome = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
