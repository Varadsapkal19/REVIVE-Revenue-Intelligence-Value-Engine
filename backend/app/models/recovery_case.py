from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base
import datetime

class RecoveryCase(Base):
    __tablename__ = "recovery_cases"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("revenue_events.id"))
    amount = Column(Float)
    risk_score = Column(Float)
    root_cause = Column(String)
    root_cause_confidence = Column(Float)
    root_cause_evidence = Column(JSONB)
    recoverable_amount = Column(Float)
    selected_action = Column(String)
    expected_recovery = Column(Float)
    natural_recovery_estimate = Column(Float)
    expected_incremental_recovery = Column(Float)
    actual_recovery = Column(Float, nullable=True)
    actual_incremental_recovery = Column(Float, nullable=True)
    fatigue_score = Column(Float)
    status = Column(String)
    guardrail_checks = Column(JSONB)
    action_ranking = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
