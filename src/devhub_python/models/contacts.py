from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class Contact(BaseModel):
    """
    Contact model representing a contact in the DevHub API.
    """

    id: str = Field(description="Unique identifier for the contact")
    account_id: Optional[str] = Field(None, description="Account identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    phone_number: Optional[str] = Field(None, description="Contact phone number in E.164 format")
    email: Optional[str] = Field(None, description="Contact email address")
    first_name: Optional[str] = Field(None, description="Contact first name")
    last_name: Optional[str] = Field(None, description="Contact last name")
    company: Optional[str] = Field(None, description="Contact company")
    address: Optional[str] = Field(None, description="Contact address")
    country_code: Optional[str] = Field(None, description="Country code")

    # Subscription preferences
    is_whatsapp_subscribed: Optional[bool] = Field(None, description="WhatsApp subscription status")
    is_email_subscribed: Optional[bool] = Field(None, description="Email subscription status")
    is_sms_subscribed: Optional[bool] = Field(None, description="SMS subscription status")
    is_mms_subscribed: Optional[bool] = Field(None, description="MMS subscription status")
    is_rcs_subscribed: Optional[bool] = Field(None, description="RCS subscription status")

    # Communication preferences
    preferred_channel: Optional[str] = Field(None, description="Preferred communication channel")
    timezone: Optional[str] = Field(None, description="Contact timezone")
    language: Optional[str] = Field(None, description="Preferred language")

    # Tags and grouping
    tags: Optional[List[str]] = Field(None, description="Contact tags")
    contacts_group_ids: Optional[List[str]] = Field(None, description="Contact group IDs")

    # Custom fields
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Custom field values")

    # Metadata
    created_at: Optional[datetime] = Field(None, description="Contact creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Contact last updated timestamp")
    last_contacted: Optional[datetime] = Field(None, description="Last contact timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class ContactSerializer(Contact):
    """Contact serializer for API responses."""

    pass


class CreateContactDto(BaseModel):
    """
    Data transfer object for creating a new contact.
    """

    phone_number: Optional[str] = Field(None, description="Contact phone number in E.164 format")
    email: Optional[str] = Field(None, description="Contact email address")
    first_name: Optional[str] = Field(None, description="Contact first name")
    last_name: Optional[str] = Field(None, description="Contact last name")
    company: Optional[str] = Field(None, description="Contact company")
    address: Optional[str] = Field(None, description="Contact address")
    country_code: Optional[str] = Field(None, description="Country code")

    # Subscription preferences
    is_whatsapp_subscribed: Optional[bool] = Field(True, description="WhatsApp subscription status")
    is_email_subscribed: Optional[bool] = Field(True, description="Email subscription status")
    is_sms_subscribed: Optional[bool] = Field(True, description="SMS subscription status")
    is_mms_subscribed: Optional[bool] = Field(True, description="MMS subscription status")
    is_rcs_subscribed: Optional[bool] = Field(True, description="RCS subscription status")

    # Communication preferences
    preferred_channel: Optional[str] = Field(None, description="Preferred communication channel")
    timezone: Optional[str] = Field(None, description="Contact timezone")
    language: Optional[str] = Field(None, description="Preferred language")

    # Tags and grouping
    tags: Optional[List[str]] = Field(None, description="Contact tags")
    contacts_group_ids: Optional[List[str]] = Field(None, description="Contact group IDs to assign")

    # Custom fields
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Custom field values")

    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    @validator("email")
    def validate_email(cls, v):
        """Validate email format if provided."""
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate phone number format if provided."""
        if v and not v.startswith("+"):
            raise ValueError("Phone number must be in E.164 format (start with +)")
        return v


class UpdateContactDto(BaseModel):
    """
    Data transfer object for updating an existing contact.
    """

    phone_number: Optional[str] = Field(None, description="Contact phone number in E.164 format")
    email: Optional[str] = Field(None, description="Contact email address")
    first_name: Optional[str] = Field(None, description="Contact first name")
    last_name: Optional[str] = Field(None, description="Contact last name")
    company: Optional[str] = Field(None, description="Contact company")
    address: Optional[str] = Field(None, description="Contact address")
    country_code: Optional[str] = Field(None, description="Country code")

    # Subscription preferences
    is_whatsapp_subscribed: Optional[bool] = Field(None, description="WhatsApp subscription status")
    is_email_subscribed: Optional[bool] = Field(None, description="Email subscription status")
    is_sms_subscribed: Optional[bool] = Field(None, description="SMS subscription status")
    is_mms_subscribed: Optional[bool] = Field(None, description="MMS subscription status")
    is_rcs_subscribed: Optional[bool] = Field(None, description="RCS subscription status")

    # Communication preferences
    preferred_channel: Optional[str] = Field(None, description="Preferred communication channel")
    timezone: Optional[str] = Field(None, description="Contact timezone")
    language: Optional[str] = Field(None, description="Preferred language")

    # Tags and grouping
    tags: Optional[List[str]] = Field(None, description="Contact tags")
    contacts_group_ids: Optional[List[str]] = Field(None, description="Contact group IDs")

    # Custom fields
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Custom field values")

    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    @validator("email")
    def validate_email(cls, v):
        """Validate email format if provided."""
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate phone number format if provided."""
        if v and not v.startswith("+"):
            raise ValueError("Phone number must be in E.164 format (start with +)")
        return v


class DeleteContactsDto(BaseModel):
    """
    Data transfer object for deleting contacts.
    """

    contact_ids: List[str] = Field(description="List of contact IDs to delete", min_length=1)

    @validator("contact_ids")
    def validate_contact_ids(cls, v):
        """Validate that contact IDs list is not empty."""
        if not v:
            raise ValueError("At least one contact ID must be provided")
        return v


class AssignToContactsGroupDto(BaseModel):
    """
    Data transfer object for assigning/unassigning contacts to/from groups.
    """

    contact_ids: List[str] = Field(description="List of contact IDs", min_length=1)
    contacts_group_id: str = Field(description="Contact group ID")

    @validator("contact_ids")
    def validate_contact_ids(cls, v):
        """Validate that contact IDs list is not empty."""
        if not v:
            raise ValueError("At least one contact ID must be provided")
        return v

    @validator("contacts_group_id")
    def validate_group_id(cls, v):
        """Validate that group ID is not empty."""
        if not v or not v.strip():
            raise ValueError("Contact group ID cannot be empty")
        return v.strip()


class CreateContactsFromCsvDto(BaseModel):
    """
    Data transfer object for importing contacts from CSV.
    """

    csv_data: str = Field(description="CSV data as string")
    contacts_group_id: Optional[str] = Field(None, description="Contact group ID to assign imported contacts")
    skip_duplicates: Optional[bool] = Field(True, description="Skip duplicate contacts")
    update_existing: Optional[bool] = Field(False, description="Update existing contacts")

    @validator("csv_data")
    def validate_csv_data(cls, v):
        """Validate that CSV data is not empty."""
        if not v or not v.strip():
            raise ValueError("CSV data cannot be empty")
        return v.strip()


class CreateContactsFromCsvRespDto(BaseModel):
    """
    Response data transfer object for CSV import operation.
    """

    total_processed: int = Field(description="Total number of contacts processed")
    successfully_created: int = Field(description="Number of contacts successfully created")
    skipped_duplicates: int = Field(description="Number of duplicate contacts skipped")
    failed_imports: int = Field(description="Number of failed imports")
    errors: Optional[List[str]] = Field(None, description="List of error messages")


class GetContactsSerializer(BaseModel):
    """
    Serializer for paginated contacts list response.
    """

    contacts: List[ContactSerializer] = Field(description="List of contacts")
    total: int = Field(description="Total number of contacts")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Number of contacts per page")
    total_pages: int = Field(description="Total number of pages")

    @validator("page")
    def validate_page(cls, v):
        """Validate page number."""
        if v < 1:
            raise ValueError("Page number must be positive")
        return v

    @validator("limit")
    def validate_limit(cls, v):
        """Validate limit."""
        if v < 1:
            raise ValueError("Limit must be positive")
        return v


# Custom Fields Models
class CustomField(BaseModel):
    """
    Custom field model.
    """

    id: str = Field(description="Unique identifier for the custom field")
    name: str = Field(description="Custom field name")
    field_type: str = Field(description="Field type (text, number, date, boolean, etc.)")
    description: Optional[str] = Field(None, description="Custom field description")
    is_required: Optional[bool] = Field(False, description="Whether the field is required")
    default_value: Optional[Any] = Field(None, description="Default value for the field")
    options: Optional[List[str]] = Field(None, description="Options for select/radio fields")
    created_at: Optional[datetime] = Field(None, description="Field creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Field last updated timestamp")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class CustomFieldSerializer(CustomField):
    """Custom field serializer for API responses."""

    pass


class CreateCustomFieldDto(BaseModel):
    """
    Data transfer object for creating a custom field.
    """

    name: str = Field(description="Custom field name")
    field_type: str = Field(description="Field type (text, number, date, boolean, etc.)")
    description: Optional[str] = Field(None, description="Custom field description")
    is_required: Optional[bool] = Field(False, description="Whether the field is required")
    default_value: Optional[Any] = Field(None, description="Default value for the field")
    options: Optional[List[str]] = Field(None, description="Options for select/radio fields")

    @validator("name")
    def validate_name(cls, v):
        """Validate field name."""
        if not v or not v.strip():
            raise ValueError("Custom field name cannot be empty")
        return v.strip()

    @validator("field_type")
    def validate_field_type(cls, v):
        """Validate field type."""
        allowed_types = ["text", "number", "date", "boolean", "select", "radio", "textarea"]
        if v not in allowed_types:
            raise ValueError(f'Field type must be one of: {", ".join(allowed_types)}')
        return v


class UpdateCustomFieldDto(BaseModel):
    """
    Data transfer object for updating a custom field.
    """

    name: Optional[str] = Field(None, description="Custom field name")
    field_type: Optional[str] = Field(None, description="Field type")
    description: Optional[str] = Field(None, description="Custom field description")
    is_required: Optional[bool] = Field(None, description="Whether the field is required")
    default_value: Optional[Any] = Field(None, description="Default value for the field")
    options: Optional[List[str]] = Field(None, description="Options for select/radio fields")

    @validator("name")
    def validate_name(cls, v):
        """Validate field name."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Custom field name cannot be empty")
        return v.strip() if v else v

    @validator("field_type")
    def validate_field_type(cls, v):
        """Validate field type."""
        if v is not None:
            allowed_types = ["text", "number", "date", "boolean", "select", "radio", "textarea"]
            if v not in allowed_types:
                raise ValueError(f'Field type must be one of: {", ".join(allowed_types)}')
        return v


class GetCustomFieldsSerializer(BaseModel):
    """
    Serializer for paginated custom fields list response.
    """

    custom_fields: List[CustomFieldSerializer] = Field(description="List of custom fields")
    total: int = Field(description="Total number of custom fields")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Number of custom fields per page")
    total_pages: int = Field(description="Total number of pages")

    @validator("page")
    def validate_page(cls, v):
        """Validate page number."""
        if v < 1:
            raise ValueError("Page number must be positive")
        return v

    @validator("limit")
    def validate_limit(cls, v):
        """Validate limit."""
        if v < 1:
            raise ValueError("Limit must be positive")
        return v


class CommonDeleteDto(BaseModel):
    """
    Common data transfer object for delete operations.
    """

    ids: List[str] = Field(description="List of IDs to delete", min_length=1)

    @validator("ids")
    def validate_ids(cls, v):
        """Validate that IDs list is not empty."""
        if not v:
            raise ValueError("At least one ID must be provided")
        return v
