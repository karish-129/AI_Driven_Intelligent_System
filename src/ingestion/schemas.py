# src/ingestion/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime

class TelemetryLog(BaseModel):
    customer_id: str = Field(..., description="Unique identifier for the bank customer")
    device_id: str = Field(..., description="Unique hardware/fingerprint ID of the device")
    ip_address: str = Field(..., description="IP address from which the session originated")
    is_vpn: bool = Field(default=False, description="Flag indicating if the connection is routed via a known VPN")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the cyber telemetry event")

class TransactionLog(BaseModel):
    customer_id: str = Field(..., description="Unique identifier for the bank customer")
    amount: float = Field(..., gt=0, description="The monetary value of the transaction")
    channel: str = Field(..., description="The transaction medium (e.g., UPI, IMPS, NetBanking)")
    beneficiary_id: str = Field(..., description="Target bank account or VPA receiving the funds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the transaction execution")