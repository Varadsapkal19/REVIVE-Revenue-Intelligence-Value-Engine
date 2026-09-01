from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base
import datetime

class RevenueEvent(Base):
    __tablename__ = "revenue_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=True)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    raw_payload = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
