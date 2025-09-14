from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


# Omni-channel send message models
class SendMessageDto(BaseModel):
    """
    Unified send message DTO for omni-channel messaging.

    Allows sending messages through any channel (SMS, Email, WhatsApp, RCS)
    with channel-specific payloads.
    """

    channel: Literal["sms", "email", "whatsapp", "rcs"] = Field(..., description="Communication channel to use")
    to: str = Field(..., description="Recipient identifier (phone/email)")
    from_: Optional[str] = Field(None, alias="from", description="Sender identifier")

    # Channel-specific payload
    payload: Dict[str, Any] = Field(..., description="Channel-specific message payload")

    # Common optional fields
    callback_url: Optional[str] = Field(None, description="Webhook URL for status updates")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        populate_by_name = True


class SendMessageSerializer(BaseModel):
    """
    Response serializer for omni-channel message sending.
    """

    id: str = Field(..., description="Message ID")
    channel: str = Field(..., description="Channel used for sending")
    to: str = Field(..., description="Recipient")
    from_: Optional[str] = Field(None, alias="from", description="Sender")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction")

    # Channel-specific content
    content: Dict[str, Any] = Field(..., description="Message content")

    # Tracking and metadata
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    created_at: datetime = Field(..., description="Creation timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        populate_by_name = True


class Message(BaseModel):
    """
    Unified message model.

    Represents a message from any channel (SMS, Email, WhatsApp, RCS)
    in the DevHub API.
    """

    id: str = Field(..., description="Unique identifier for the message")
    account_id: Optional[str] = Field(None, description="Account identifier")
    channel: str = Field(..., description="Communication channel (sms, email, whatsapp, rcs)")
    type: str = Field(..., description="Message type")

    # Recipient/sender information
    to: str = Field(..., description="Recipient identifier (phone/email)")
    from_: Optional[str] = Field(None, alias="from", description="Sender identifier")

    # Message content (varies by channel)
    content: Dict[str, Any] = Field(..., description="Message content (channel-specific)")

    # Status and delivery
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")

    # Delivery tracking
    delivery_status: Optional[Dict[str, Any]] = Field(None, description="Detailed delivery status")

    # Pricing and billing
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")

    # Error handling
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")

    # Timestamps
    date_created: Optional[datetime] = Field(None, description="Message creation timestamp")
    date_sent: Optional[datetime] = Field(None, description="Message sent timestamp")
    date_delivered: Optional[datetime] = Field(None, description="Message delivered timestamp")
    date_read: Optional[datetime] = Field(None, description="Message read timestamp")
    date_updated: Optional[datetime] = Field(None, description="Message last updated timestamp")

    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
