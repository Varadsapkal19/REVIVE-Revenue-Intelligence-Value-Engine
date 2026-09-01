from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base
import datetime

class Payment(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    order_id = Column(UUID(as_uuid=True), nullable=True)
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String)
    failure_reason = Column(String, nullable=True)
    payment_method = Column(String)
    gateway = Column(String, default="razorpay")
    razorpay_payment_id = Column(String, nullable=True)
    metadata_ = Column("metadata", JSONB)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
