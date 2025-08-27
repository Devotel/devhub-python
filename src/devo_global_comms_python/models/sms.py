from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SMSMessage(BaseModel):
    """
    SMS message model.

    Represents an SMS message sent through the Devo Global Communications API.
    """

    sid: str = Field(..., description="Unique identifier for the message")
    account_sid: Optional[str] = Field(None, description="Account identifier")
    to: str = Field(..., description="Recipient phone number in E.164 format")
    from_: Optional[str] = Field(None, alias="from", description="Sender phone number")
    body: str = Field(..., description="Message body text")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")
    price: Optional[str] = Field(None, description="Message price")
    price_unit: Optional[str] = Field(None, description="Price currency unit")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    num_segments: Optional[int] = Field(None, description="Number of message segments")
    media_urls: Optional[List[str]] = Field(None, description="URLs of attached media")
    date_created: Optional[datetime] = Field(
        None, description="Message creation timestamp"
    )
    date_sent: Optional[datetime] = Field(None, description="Message sent timestamp")
    date_updated: Optional[datetime] = Field(
        None, description="Message last updated timestamp"
    )
    messaging_service_sid: Optional[str] = Field(
        None, description="Messaging service identifier"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
