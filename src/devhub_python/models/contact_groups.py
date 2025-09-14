from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ContactsGroup(BaseModel):
    """
    Contact group model representing a collection of contacts.
    """

    id: str = Field(description="Unique identifier for the contact group")
    name: str = Field(description="Name of the contact group")
    description: Optional[str] = Field(None, description="Description of the contact group")
    contacts_count: Optional[int] = Field(None, description="Number of contacts in the group")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    user_id: Optional[str] = Field(None, description="ID of the user who owns the group")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class CreateContactsGroupDto(BaseModel):
    """
    DTO for creating a new contact group.
    """

    name: str = Field(description="Name of the contact group", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Description of the contact group", max_length=1000)
    contact_ids: Optional[List[str]] = Field(None, description="List of contact IDs to add to the group")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class UpdateContactsGroupDto(BaseModel):
    """
    DTO for updating an existing contact group.
    """

    name: Optional[str] = Field(None, description="Updated name of the contact group", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Updated description of the contact group", max_length=1000)
    contact_ids: Optional[List[str]] = Field(None, description="Updated list of contact IDs")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata")


class DeleteContactsGroupsDto(BaseModel):
    """
    DTO for bulk deleting contact groups.
    """

    group_ids: List[str] = Field(description="List of contact group IDs to delete", min_length=1)
    transfer_contacts_to: Optional[str] = Field(None, description="Group ID to transfer contacts to before deletion")


class ContactsGroupListResponse(BaseModel):
    """
    Response model for listing contact groups with pagination.
    """

    groups: List[ContactsGroup] = Field(description="List of contact groups")
    total: int = Field(description="Total number of groups")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")
