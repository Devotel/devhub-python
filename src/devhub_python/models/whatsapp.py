from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


# Template Component Models
class TemplateExample(BaseModel):
    """Example values for template variables"""

    header_text: Optional[List[str]] = None
    body_text: Optional[List[List[str]]] = None
    header_handle: Optional[List[str]] = None


class OTPButton(BaseModel):
    """OTP button for authentication templates"""

    type: Literal["OTP"] = "OTP"
    otp_type: Literal["COPY_CODE", "ONE_TAP"]
    text: str
    autofill_text: Optional[str] = None
    package_name: Optional[str] = None
    signature_hash: Optional[str] = None


class CatalogButton(BaseModel):
    """Catalog button for marketing templates"""

    type: Literal["CATALOG"] = "CATALOG"
    text: str


class MPMButton(BaseModel):
    """Multi-Product Message button"""

    type: Literal["MPM"] = "MPM"
    text: str


class QuickReplyButton(BaseModel):
    """Quick reply button"""

    type: Literal["QUICK_REPLY"] = "QUICK_REPLY"
    text: str


class PhoneNumberButton(BaseModel):
    """Phone number button"""

    type: Literal["PHONE_NUMBER"] = "PHONE_NUMBER"
    text: str
    phone_number: str


class URLButton(BaseModel):
    """URL button with dynamic parameters"""

    type: Literal["URL"] = "URL"
    text: str
    url: str
    example: Optional[List[str]] = None


class HeaderComponent(BaseModel):
    """Header component with different formats"""

    type: Literal["HEADER"] = "HEADER"
    format: Literal["TEXT", "IMAGE", "DOCUMENT", "LOCATION"]
    text: Optional[str] = None
    example: Optional[TemplateExample] = None


class BodyComponent(BaseModel):
    """Body component with text and examples"""

    type: Literal["BODY"] = "BODY"
    text: Optional[str] = None
    add_security_recommendation: Optional[bool] = None
    example: Optional[TemplateExample] = None


class FooterComponent(BaseModel):
    """Footer component"""

    type: Literal["FOOTER"] = "FOOTER"
    text: Optional[str] = None
    code_expiration_minutes: Optional[int] = None


class ButtonsComponent(BaseModel):
    """Buttons component containing various button types"""

    type: Literal["BUTTONS"] = "BUTTONS"
    buttons: List[Union[OTPButton, CatalogButton, MPMButton, QuickReplyButton, PhoneNumberButton, URLButton]]


class WhatsAppTemplateRequest(BaseModel):
    """WhatsApp template creation request"""

    name: str = Field(description="Template name")
    language: str = Field(description="Template language code (e.g., 'en_US', 'en')")
    category: Literal["AUTHENTICATION", "MARKETING", "UTILITY"] = Field(description="Template category")
    components: List[Union[HeaderComponent, BodyComponent, FooterComponent, ButtonsComponent]] = Field(
        description="Template components"
    )


class WhatsAppTemplateResponse(BaseModel):
    """WhatsApp template creation response"""

    id: str = Field(description="Template ID")
    name: str = Field(description="Template name")
    language: str = Field(description="Template language")
    category: str = Field(description="Template category")
    status: str = Field(description="Template status")
    components: List[Any] = Field(description="Template components")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Update timestamp")


class GetWhatsAppTemplatesResponse(BaseModel):
    """Response for getting WhatsApp templates with pagination"""

    templates: List["WhatsAppTemplate"] = Field(description="List of templates")
    total: int = Field(description="Total number of templates")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Page limit")
    has_next: bool = Field(description="Whether there are more pages")


# Template Message Sending Models
class ImageParameter(BaseModel):
    """Image parameter for template messages"""

    link: str = Field(description="Image URL")


class DocumentParameter(BaseModel):
    """Document parameter for template messages"""

    link: str = Field(description="Document URL")
    filename: Optional[str] = Field(None, description="Document filename")


class LocationParameter(BaseModel):
    """Location parameter for template messages"""

    latitude: str = Field(description="Latitude coordinate")
    longitude: str = Field(description="Longitude coordinate")
    name: Optional[str] = Field(None, description="Location name")
    address: Optional[str] = Field(None, description="Location address")


class TemplateMessageParameter(BaseModel):
    """Parameter for template message components"""

    type: Literal["text", "image", "location", "document", "payload"]
    text: Optional[str] = Field(None, description="Text parameter value")
    image: Optional[ImageParameter] = Field(None, description="Image parameter")
    location: Optional[LocationParameter] = Field(None, description="Location parameter")
    document: Optional[DocumentParameter] = Field(None, description="Document parameter")
    payload: Optional[str] = Field(None, description="Payload parameter value")


class TemplateMessageComponent(BaseModel):
    """Component for template message"""

    type: Literal["header", "body", "button"]
    sub_type: Optional[Literal["url", "quick_reply", "phone_number"]] = Field(None, description="Button sub-type")
    index: Optional[str] = Field(None, description="Button index")
    parameters: List[TemplateMessageParameter] = Field(description="Component parameters")


class TemplateMessageLanguage(BaseModel):
    """Language specification for template message"""

    code: str = Field(description="Language code (e.g., 'en_US', 'en')")


class TemplateMessageTemplate(BaseModel):
    """Template specification for template message"""

    name: str = Field(description="Template name")
    language: TemplateMessageLanguage = Field(description="Template language")
    components: Optional[List[TemplateMessageComponent]] = Field(
        None, description="Template components with parameters"
    )


class WhatsAppTemplateMessageRequest(BaseModel):
    """Request for sending WhatsApp template message"""

    messaging_product: Literal["whatsapp"] = "whatsapp"
    to: str = Field(description="Recipient phone number")
    type: Literal["template"] = "template"
    template: TemplateMessageTemplate = Field(description="Template configuration")


class WhatsAppTemplateMessageResponse(BaseModel):
    """Response for WhatsApp template message send"""

    message_id: str = Field(description="Unique message identifier")
    status: str = Field(description="Message status")
    to: str = Field(description="Recipient phone number")
    account_id: str = Field(description="WhatsApp account ID used")
    timestamp: datetime = Field(description="Message send timestamp")
    success: bool = Field(description="Whether the message was sent successfully")


# Request Models
class WhatsAppNormalMessageRequest(BaseModel):
    """
    Request model for WhatsApp normal message send.

    Used for POST /api/v1/user-api/whatsapp/send-normal-message
    """

    to: str = Field(..., description="Recipient phone number in E.164 format")
    message: str = Field(..., description="Message content")
    account_id: Optional[str] = Field(None, description="WhatsApp account ID to send from")


class FileUploadRequest(BaseModel):
    """
    Request model for WhatsApp file upload.

    Used for POST /api/v1/user-api/whatsapp/upload
    """

    file: bytes = Field(..., description="File content to upload")
    filename: str = Field(..., description="Name of the file")
    content_type: str = Field(..., description="MIME type of the file")


# Response Models
class WhatsAppAccount(BaseModel):
    """WhatsApp account information model."""

    id: Optional[str] = Field(None, description="Account ID")
    name: Optional[str] = Field(None, description="Account name")
    email: Optional[str] = Field(None, description="Account email")
    phone: Optional[str] = Field(None, description="Account phone number")
    is_approved: Optional[bool] = Field(None, description="Whether the account is approved")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Account last updated timestamp")
    # Additional fields that might be present in the API response
    totalTemplates: Optional[int] = Field(None, description="Total number of templates")

    class Config:
        populate_by_name = True

    @classmethod
    def model_validate(cls, obj):
        # Handle _id -> id mapping for API compatibility
        if isinstance(obj, dict) and "_id" in obj and "id" not in obj:
            obj = obj.copy()
            obj["id"] = obj["_id"]
        return super().model_validate(obj)


class GetWhatsAppAccountsResponse(BaseModel):
    """
    Response model for getting WhatsApp accounts.

    Returned from GET /api/v1/user-api/whatsapp/accounts
    """

    accounts: List[WhatsAppAccount] = Field(default_factory=list, description="List of WhatsApp accounts")
    total: Optional[int] = Field(None, description="Total number of accounts")
    page: Optional[int] = Field(None, description="Current page number")
    limit: Optional[int] = Field(None, description="Page size limit")
    has_next: Optional[bool] = Field(None, description="Whether there are more pages")


class WhatsAppTemplate(BaseModel):
    """
    WhatsApp template model.

    Returned from GET /api/v1/user-api/whatsapp/templates/{name}
    """

    name: str = Field(..., description="Template name")
    language: str = Field(..., description="Template language code")
    status: str = Field(..., description="Template status")
    category: str = Field(..., description="Template category")
    components: List[Dict[str, Any]] = Field(..., description="Template components")
    created_at: Optional[datetime] = Field(None, description="Template creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Template last updated timestamp")


class WhatsAppUploadFileResponse(BaseModel):
    """
    Response model for WhatsApp file upload.

    Returned from POST /api/v1/user-api/whatsapp/upload
    """

    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of the file")
    url: str = Field(..., description="File URL")
    expires_at: Optional[datetime] = Field(None, description="File expiration timestamp")


class WhatsAppSendMessageResponse(BaseModel):
    """
    Response model for WhatsApp message send.

    Returned from POST /api/v1/user-api/whatsapp/send-normal-message
    """

    message_id: str = Field(..., description="Unique message identifier")
    status: str = Field(..., description="Message status")
    to: str = Field(..., description="Recipient phone number")
    account_id: str = Field(..., description="WhatsApp account ID used")
    timestamp: datetime = Field(..., description="Message send timestamp")
    success: bool = Field(..., description="Whether the message was sent successfully")


class WhatsAppMessage(BaseModel):
    """
    WhatsApp message model.

    Represents a WhatsApp message sent through the DevHub API.
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
    template: Optional[Dict[str, Any]] = Field(None, description="Template message content")
    media: Optional[Dict[str, Any]] = Field(None, description="Media message content")

    # Metadata
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    date_created: Optional[datetime] = Field(None, description="Message creation timestamp")
    date_sent: Optional[datetime] = Field(None, description="Message sent timestamp")
    date_delivered: Optional[datetime] = Field(None, description="Message delivered timestamp")
    date_read: Optional[datetime] = Field(None, description="Message read timestamp")
    date_updated: Optional[datetime] = Field(None, description="Message last updated timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
