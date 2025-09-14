from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Account Management Models
class SubmitRcsAccountDto(BaseModel):
    """Model for submitting a new RCS account."""

    name: str = Field(..., description="Account name")
    brand_name: str = Field(..., description="Brand name for the account")
    business_description: str = Field(..., description="Business description")
    contact_email: str = Field(..., description="Contact email address")
    contact_phone: str = Field(..., description="Contact phone number")
    website_url: Optional[str] = Field(None, description="Website URL")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    privacy_policy_url: Optional[str] = Field(None, description="Privacy policy URL")
    terms_of_service_url: Optional[str] = Field(None, description="Terms of service URL")


class VerificationRcsAccountDto(BaseModel):
    """Model for verifying an RCS account."""

    account_id: str = Field(..., description="Account ID to verify")
    verification_code: str = Field(..., description="Verification code")


class UpdateRcsAccountDto(BaseModel):
    """Model for updating an RCS account."""

    name: Optional[str] = Field(None, description="Account name")
    brand_name: Optional[str] = Field(None, description="Brand name")
    business_description: Optional[str] = Field(None, description="Business description")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    website_url: Optional[str] = Field(None, description="Website URL")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    privacy_policy_url: Optional[str] = Field(None, description="Privacy policy URL")
    terms_of_service_url: Optional[str] = Field(None, description="Terms of service URL")


class RcsAccountSerializer(BaseModel):
    """Serializer for RCS account data."""

    id: str = Field(..., description="Account ID")
    name: str = Field(..., description="Account name")
    brand_name: str = Field(..., description="Brand name")
    business_description: str = Field(..., description="Business description")
    contact_email: str = Field(..., description="Contact email")
    contact_phone: str = Field(..., description="Contact phone")
    website_url: Optional[str] = Field(None, description="Website URL")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    privacy_policy_url: Optional[str] = Field(None, description="Privacy policy URL")
    terms_of_service_url: Optional[str] = Field(None, description="Terms of service URL")
    is_approved: bool = Field(..., description="Account approval status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Account last update timestamp")


# Template Management Models
class CreateRcsTemplateDto(BaseModel):
    """Model for creating an RCS template."""

    name: str = Field(..., description="Template name")
    title: str = Field(..., description="Template title")
    description: str = Field(..., description="Template description")
    content: Dict[str, Any] = Field(..., description="Template content structure")
    category: str = Field(..., description="Template category")
    account_id: str = Field(..., description="Associated account ID")


class UpdateRcsTemplateDto(BaseModel):
    """Model for updating an RCS template."""

    name: Optional[str] = Field(None, description="Template name")
    title: Optional[str] = Field(None, description="Template title")
    description: Optional[str] = Field(None, description="Template description")
    content: Optional[Dict[str, Any]] = Field(None, description="Template content structure")
    category: Optional[str] = Field(None, description="Template category")


class RcsTemplateSerializer(BaseModel):
    """Serializer for RCS template data."""

    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    title: str = Field(..., description="Template title")
    description: str = Field(..., description="Template description")
    content: Dict[str, Any] = Field(..., description="Template content structure")
    category: str = Field(..., description="Template category")
    account_id: str = Field(..., description="Associated account ID")
    status: str = Field(..., description="Template status")
    created_at: datetime = Field(..., description="Template creation timestamp")
    updated_at: datetime = Field(..., description="Template last update timestamp")


# Brand Management Models
class UpsertRcsBrandDto(BaseModel):
    """Model for creating or updating an RCS brand."""

    name: str = Field(..., description="Brand name")
    description: str = Field(..., description="Brand description")
    logo_url: Optional[str] = Field(None, description="Brand logo URL")
    primary_color: Optional[str] = Field(None, description="Primary brand color")
    secondary_color: Optional[str] = Field(None, description="Secondary brand color")
    website_url: Optional[str] = Field(None, description="Brand website URL")
    account_id: str = Field(..., description="Associated account ID")


class RcsBrandSerializer(BaseModel):
    """Serializer for RCS brand data."""

    id: str = Field(..., description="Brand ID")
    name: str = Field(..., description="Brand name")
    description: str = Field(..., description="Brand description")
    logo_url: Optional[str] = Field(None, description="Brand logo URL")
    primary_color: Optional[str] = Field(None, description="Primary brand color")
    secondary_color: Optional[str] = Field(None, description="Secondary brand color")
    website_url: Optional[str] = Field(None, description="Brand website URL")
    account_id: str = Field(..., description="Associated account ID")
    created_at: datetime = Field(..., description="Brand creation timestamp")
    updated_at: datetime = Field(..., description="Brand last update timestamp")


# Tester Management Models
class RcsTesterDto(BaseModel):
    """Model for adding an RCS tester."""

    phone_number: str = Field(..., description="Tester phone number in E.164 format")
    name: str = Field(..., description="Tester name")
    email: str = Field(..., description="Tester email address")
    account_id: str = Field(..., description="Associated account ID")


class RcsTesterSerializer(BaseModel):
    """Serializer for RCS tester data."""

    id: str = Field(..., description="Tester ID")
    phone_number: str = Field(..., description="Tester phone number")
    name: str = Field(..., description="Tester name")
    email: str = Field(..., description="Tester email address")
    account_id: str = Field(..., description="Associated account ID")
    status: str = Field(..., description="Tester status")
    created_at: datetime = Field(..., description="Tester creation timestamp")


# Messaging Models
class RcsMessageDto(BaseModel):
    """Model for sending an RCS message."""

    to: str = Field(..., description="Recipient phone number in E.164 format")
    from_: Optional[str] = Field(None, alias="from", description="Sender phone number")
    account_id: str = Field(..., description="Account ID")
    message_type: str = Field(..., description="Message type (text, rich_card, carousel)")

    # Text message content
    text: Optional[str] = Field(None, description="Text message content")

    # Rich card content
    rich_card: Optional[Dict[str, Any]] = Field(None, description="Rich card content")

    # Carousel content
    carousel: Optional[Dict[str, Any]] = Field(None, description="Carousel content")

    # Media and attachments
    media_url: Optional[str] = Field(None, description="Media URL")

    # Interactive elements
    actions: Optional[List[Dict[str, Any]]] = Field(None, description="Available actions")
    suggestions: Optional[List[Dict[str, Any]]] = Field(None, description="Suggested replies")

    # Callback and metadata
    callback_url: Optional[str] = Field(None, description="Callback URL for status updates")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")


class RcsSendMessageSerializer(BaseModel):
    """Serializer for RCS message send response."""

    id: str = Field(..., description="Message ID")
    account_id: str = Field(..., description="Account ID")
    to: str = Field(..., description="Recipient phone number")
    from_: Optional[str] = Field(None, alias="from", description="Sender phone number")
    message_type: str = Field(..., description="Message type")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction")

    # Content
    text: Optional[str] = Field(None, description="Text content")
    rich_card: Optional[Dict[str, Any]] = Field(None, description="Rich card content")
    carousel: Optional[Dict[str, Any]] = Field(None, description="Carousel content")
    media_url: Optional[str] = Field(None, description="Media URL")
    actions: Optional[List[Dict[str, Any]]] = Field(None, description="Actions")
    suggestions: Optional[List[Dict[str, Any]]] = Field(None, description="Suggestions")

    # Metadata and timestamps
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(..., description="Message creation timestamp")
    sent_at: Optional[datetime] = Field(None, description="Message sent timestamp")
    delivered_at: Optional[datetime] = Field(None, description="Message delivered timestamp")
    read_at: Optional[datetime] = Field(None, description="Message read timestamp")
    updated_at: datetime = Field(..., description="Message last update timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")


# Generic Models
class DeleteDto(BaseModel):
    """Model for deletion requests."""

    ids: List[str] = Field(..., description="List of IDs to delete")
    reason: Optional[str] = Field(None, description="Reason for deletion")


class SuccessSerializer(BaseModel):
    """Generic success response serializer."""

    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class RCSMessage(BaseModel):
    """
    RCS (Rich Communication Services) message model.

    Represents an RCS message sent through the DevHub API.
    """

    id: str = Field(..., description="Unique identifier for the message")
    account_id: Optional[str] = Field(None, description="Account identifier")
    to: str = Field(..., description="Recipient phone number in E.164 format")
    from_: Optional[str] = Field(None, alias="from", description="Sender phone number")
    type: str = Field(..., description="Message type (text, rich_card, carousel, etc.)")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")

    # Content fields
    text: Optional[str] = Field(None, description="Text message content")
    rich_card: Optional[Dict[str, Any]] = Field(None, description="Rich card content")
    carousel: Optional[Dict[str, Any]] = Field(None, description="Carousel content")
    media_url: Optional[str] = Field(None, description="Media URL")

    # Interaction data
    actions: Optional[List[Dict[str, Any]]] = Field(None, description="Available actions")
    suggestions: Optional[List[Dict[str, Any]]] = Field(None, description="Suggested replies")

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


# Apply common configuration to all models
for model_class in [
    SubmitRcsAccountDto,
    VerificationRcsAccountDto,
    UpdateRcsAccountDto,
    RcsAccountSerializer,
    CreateRcsTemplateDto,
    UpdateRcsTemplateDto,
    RcsTemplateSerializer,
    UpsertRcsBrandDto,
    RcsBrandSerializer,
    RcsTesterDto,
    RcsTesterSerializer,
    RcsMessageDto,
    RcsSendMessageSerializer,
    DeleteDto,
    SuccessSerializer,
]:
    model_class.Config = type(
        "Config",
        (),
        {"allow_population_by_field_name": True, "json_encoders": {datetime: lambda v: v.isoformat() if v else None}},
    )
