from datetime import datetime
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Unified message model.

    Represents a message from any channel (SMS, Email, WhatsApp, RCS)
    in the Devo Global Communications API.
    """

    id: str = Field(..., description="Unique identifier for the message")
    account_id: Optional[str] = Field(None, description="Account identifier")
    channel: str = Field(
        ..., description="Communication channel (sms, email, whatsapp, rcs)"
    )
    type: str = Field(..., description="Message type")

    # Recipient/sender information
    to: str = Field(..., description="Recipient identifier (phone/email)")
    from_: Optional[str] = Field(None, alias="from", description="Sender identifier")

    # Message content (varies by channel)
    content: Dict[str, Any] = Field(
        ..., description="Message content (channel-specific)"
    )

    # Status and delivery
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")

    # Delivery tracking
    delivery_status: Optional[Dict[str, Any]] = Field(
        None, description="Detailed delivery status"
    )

    # Pricing and billing
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")

    # Error handling
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")

    # Timestamps
    date_created: Optional[datetime] = Field(
        None, description="Message creation timestamp"
    )
    date_sent: Optional[datetime] = Field(None, description="Message sent timestamp")
    date_delivered: Optional[datetime] = Field(
        None, description="Message delivered timestamp"
    )
    date_read: Optional[datetime] = Field(None, description="Message read timestamp")
    date_updated: Optional[datetime] = Field(
        None, description="Message last updated timestamp"
    )

    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
