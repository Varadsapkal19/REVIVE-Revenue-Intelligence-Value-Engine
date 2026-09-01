from sqlalchemy import Column, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base
import datetime

class MerchantPolicy(Base):
    __tablename__ = "merchant_policies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    merchant_id = Column(UUID(as_uuid=True))
    max_discount_pct = Column(Float, default=10.0)
    max_outreach_per_day = Column(Integer, default=3)
    allowed_channels = Column(JSONB)
    max_autonomous_amount = Column(Float, default=50000.0)
    human_approval_threshold = Column(Float, default=100000.0)
    recovery_window_hours = Column(Integer, default=72)
    max_retry_attempts = Column(Integer, default=3)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
