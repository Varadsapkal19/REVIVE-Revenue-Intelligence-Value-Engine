from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
import datetime

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    merchant_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    external_id = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    segment = Column(String)
    payment_history_score = Column(Float)
    lifetime_value = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
