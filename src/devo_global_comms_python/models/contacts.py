from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Contact(BaseModel):
    """
    Contact model.

    Represents a contact in the Devo Global Communications API.
    """

    id: str = Field(..., description="Unique identifier for the contact")
    account_id: Optional[str] = Field(None, description="Account identifier")
    phone_number: Optional[str] = Field(
        None, description="Contact phone number in E.164 format"
    )
    email: Optional[str] = Field(None, description="Contact email address")
    first_name: Optional[str] = Field(None, description="Contact first name")
    last_name: Optional[str] = Field(None, description="Contact last name")
    company: Optional[str] = Field(None, description="Contact company")

    # Preference settings
    opt_in_sms: bool = Field(True, description="SMS opt-in status")
    opt_in_email: bool = Field(True, description="Email opt-in status")
    opt_in_whatsapp: bool = Field(True, description="WhatsApp opt-in status")
    opt_in_rcs: bool = Field(True, description="RCS opt-in status")

    # Communication preferences
    preferred_channel: Optional[str] = Field(
        None, description="Preferred communication channel"
    )
    timezone: Optional[str] = Field(None, description="Contact timezone")
    language: Optional[str] = Field(None, description="Preferred language")

    # Tags and grouping
    tags: Optional[list] = Field(None, description="Contact tags")
    groups: Optional[list] = Field(None, description="Contact groups")

    # Metadata
    date_created: Optional[datetime] = Field(
        None, description="Contact creation timestamp"
    )
    date_updated: Optional[datetime] = Field(
        None, description="Contact last updated timestamp"
    )
    last_contacted: Optional[datetime] = Field(
        None, description="Last contact timestamp"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
