from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Request Models
class EmailSendRequest(BaseModel):
    """
    Request model for email send API.

    Used for POST /user-api/email/send
    """

    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")
    sender: str = Field(..., description="Sender email address")
    recipient: str = Field(..., description="Recipient email address")


# Response Models
class EmailSendResponse(BaseModel):
    """
    Response model for email send API.

    Returned from POST /user-api/email/send
    """

    success: bool = Field(..., description="Whether the email was sent successfully")
    message_id: str = Field(..., description="Unique message identifier")
    bulk_email_id: str = Field(..., description="Bulk email identifier")
    subject: str = Field(..., description="Email subject")
    status: str = Field(..., description="Message status")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(..., description="Timestamp of the response")


class EmailAttachment(BaseModel):
    """Email attachment model."""

    filename: str = Field(..., description="Attachment filename")
    content_type: str = Field(..., description="MIME content type")
    size: int = Field(..., description="File size in bytes")
    content_id: Optional[str] = Field(None, description="Content ID for inline attachments")


class EmailMessage(BaseModel):
    """
    Email message model.

    Represents an email message sent through the Devo Global Communications API.
    """

    id: str = Field(..., description="Unique identifier for the message")
    account_id: Optional[str] = Field(None, description="Account identifier")
    to: str = Field(..., description="Recipient email address")
    from_: Optional[str] = Field(None, alias="from", description="Sender email address")
    cc: Optional[List[str]] = Field(None, description="CC email addresses")
    bcc: Optional[List[str]] = Field(None, description="BCC email addresses")
    reply_to: Optional[str] = Field(None, description="Reply-to email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Plain text email body")
    html_body: Optional[str] = Field(None, description="HTML email body")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")
    attachments: Optional[List[EmailAttachment]] = Field(None, description="Email attachments")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    date_created: Optional[datetime] = Field(None, description="Message creation timestamp")
    date_sent: Optional[datetime] = Field(None, description="Message sent timestamp")
    date_delivered: Optional[datetime] = Field(None, description="Message delivered timestamp")
    date_opened: Optional[datetime] = Field(None, description="Message opened timestamp")
    date_clicked: Optional[datetime] = Field(None, description="Link clicked timestamp")
    date_updated: Optional[datetime] = Field(None, description="Message last updated timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        validate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
