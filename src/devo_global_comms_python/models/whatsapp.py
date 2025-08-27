from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class WhatsAppMessage(BaseModel):
    """
    WhatsApp message model.

    Represents a WhatsApp message sent through the Devo Global Communications API.
    """

    id: str = Field(..., description="Unique identifier for the message")
    account_id: Optional[str] = Field(None, description="Account identifier")
    to: str = Field(..., description="Recipient phone number in E.164 format")
    from_: Optional[str] = Field(None, alias="from", description="Sender phone number")
    type: str = Field(..., description="Message type (text, template, media, etc.)")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")

    # Content fields
    text: Optional[Dict[str, str]] = Field(None, description="Text message content")
    template: Optional[Dict[str, Any]] = Field(
        None, description="Template message content"
    )
    media: Optional[Dict[str, Any]] = Field(None, description="Media message content")

    # Metadata
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
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
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
