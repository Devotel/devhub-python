from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.contacts import (
        AssignToContactsGroupDto,
        CommonDeleteDto,
        ContactSerializer,
        CreateContactDto,
        CreateContactsFromCsvDto,
        CreateContactsFromCsvRespDto,
        CreateCustomFieldDto,
        CustomFieldSerializer,
        DeleteContactsDto,
        GetContactsSerializer,
        GetCustomFieldsSerializer,
        UpdateContactDto,
        UpdateCustomFieldDto,
    )


class ContactsResource(BaseResource):
    """
    Contacts resource for managing contact information and custom fields.

    This resource provides comprehensive contact management capabilities including:
    - CRUD operations for contacts
    - Contact group assignment/unassignment
    - Custom field management
    - CSV import functionality
    - Advanced filtering and search
    """

    # Contact CRUD Operations

    def list(
        self,
        page: int = 1,
        limit: int = 50,
        contacts_group_ids: Optional[List[str]] = None,
        country_codes: Optional[List[str]] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
        is_whatsapp_subscribed: Optional[bool] = None,
        is_email_subscribed: Optional[bool] = None,
        is_sms_subscribed: Optional[bool] = None,
        is_mms_subscribed: Optional[bool] = None,
        is_rcs_subscribed: Optional[bool] = None,
        tags: Optional[List[str]] = None,
    ) -> "GetContactsSerializer":
        """
        List contacts with advanced filtering options.

        Args:
            page: Page number for pagination
            limit: Number of contacts per page
            contacts_group_ids: Filter by contact group IDs
            country_codes: Filter by country codes
            search: Search query for name, email, phone, or address
            search_fields: Specific fields to search in
            is_whatsapp_subscribed: Filter by WhatsApp subscription status
            is_email_subscribed: Filter by email subscription status
            is_sms_subscribed: Filter by SMS subscription status
            is_mms_subscribed: Filter by MMS subscription status
            is_rcs_subscribed: Filter by RCS subscription status
            tags: Filter by tags

        Returns:
            GetContactsSerializer: Paginated list of contacts
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}

        if contacts_group_ids:
            params["contacts_group_ids"] = contacts_group_ids
        if country_codes:
            params["country_codes"] = country_codes
        if search:
            params["search"] = search
        if search_fields:
            params["search_fields"] = search_fields
        if is_whatsapp_subscribed is not None:
            params["is_whatsapp_subscribed"] = is_whatsapp_subscribed
        if is_email_subscribed is not None:
            params["is_email_subscribed"] = is_email_subscribed
        if is_sms_subscribed is not None:
            params["is_sms_subscribed"] = is_sms_subscribed
        if is_mms_subscribed is not None:
            params["is_mms_subscribed"] = is_mms_subscribed
        if is_rcs_subscribed is not None:
            params["is_rcs_subscribed"] = is_rcs_subscribed
        if tags:
            params["tags"] = tags

        response = self.client.get("user-api/contacts", params=params)

        from ..models.contacts import GetContactsSerializer

        return GetContactsSerializer.parse_obj(response.json())

    def create(self, contact_data: "CreateContactDto") -> "ContactSerializer":
        """
        Create a new contact.

        Args:
            contact_data: Contact creation data

        Returns:
            ContactSerializer: Created contact
        """
        response = self.client.post("user-api/contacts", json=contact_data.dict(exclude_none=True))

        from ..models.contacts import ContactSerializer

        return ContactSerializer.parse_obj(response.json())

    def update(self, contact_id: str, contact_data: "UpdateContactDto") -> "ContactSerializer":
        """
        Update an existing contact.

        Args:
            contact_id: ID of the contact to update
            contact_data: Contact update data

        Returns:
            ContactSerializer: Updated contact
        """
        contact_id = validate_required_string(contact_id, "contact_id")

        response = self.client.put(f"user-api/contacts/{contact_id}", json=contact_data.dict(exclude_none=True))

        from ..models.contacts import ContactSerializer

        return ContactSerializer.parse_obj(response.json())

    def delete_bulk(self, delete_data: "DeleteContactsDto", approve: Optional[str] = None) -> "ContactSerializer":
        """
        Delete multiple contacts.

        Args:
            delete_data: Data containing contact IDs to delete
            approve: Approval confirmation (optional)

        Returns:
            ContactSerializer: Response from delete operation
        """
        params = {}
        if approve:
            params["approve"] = approve

        response = self.client.delete("user-api/contacts", json=delete_data.dict(), params=params)

        from ..models.contacts import ContactSerializer

        return ContactSerializer.parse_obj(response.json())

    # Contact Group Management

    def assign_to_group(self, assignment_data: "AssignToContactsGroupDto") -> None:
        """
        Assign contacts to a contact group.

        Args:
            assignment_data: Data containing contact IDs and group ID
        """
        self.client.patch("user-api/contacts/assign-to-group", json=assignment_data.dict())

    def unassign_from_group(self, assignment_data: "AssignToContactsGroupDto") -> None:
        """
        Unassign contacts from a contact group.

        Args:
            assignment_data: Data containing contact IDs and group ID
        """
        self.client.patch("user-api/contacts/unassign-from-group", json=assignment_data.dict())

    # CSV Import

    def import_from_csv(
        self, csv_data: "CreateContactsFromCsvDto", approve: Optional[str] = None
    ) -> "CreateContactsFromCsvRespDto":
        """
        Import contacts from CSV data.

        Args:
            csv_data: CSV import data
            approve: Approval confirmation (optional)

        Returns:
            CreateContactsFromCsvRespDto: Import operation results
        """
        params = {}
        if approve:
            params["approve"] = approve

        response = self.client.post("user-api/contacts/csv", json=csv_data.dict(), params=params)

        from ..models.contacts import CreateContactsFromCsvRespDto

        return CreateContactsFromCsvRespDto.parse_obj(response.json())

    # Custom Fields Management

    def list_custom_fields(
        self,
        id: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
        search: Optional[str] = None,
    ) -> "GetCustomFieldsSerializer":
        """
        List custom fields.

        Args:
            id: Specific custom field ID to retrieve
            page: Page number for pagination
            limit: Number of custom fields per page
            search: Search query for custom fields

        Returns:
            GetCustomFieldsSerializer: Paginated list of custom fields
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}

        if id:
            params["id"] = id
        if search:
            params["search"] = search

        response = self.client.get("user-api/contacts/custom-fields", params=params)

        from ..models.contacts import GetCustomFieldsSerializer

        return GetCustomFieldsSerializer.parse_obj(response.json())

    def create_custom_field(self, field_data: "CreateCustomFieldDto") -> "CustomFieldSerializer":
        """
        Create a new custom field.

        Args:
            field_data: Custom field creation data

        Returns:
            CustomFieldSerializer: Created custom field
        """
        response = self.client.post("user-api/contacts/custom-fields", json=field_data.dict())

        from ..models.contacts import CustomFieldSerializer

        return CustomFieldSerializer.parse_obj(response.json())

    def update_custom_field(self, field_id: str, field_data: "UpdateCustomFieldDto") -> None:
        """
        Update an existing custom field.

        Args:
            field_id: ID of the custom field to update
            field_data: Custom field update data
        """
        field_id = validate_required_string(field_id, "field_id")

        self.client.put(f"user-api/contacts/custom-fields/{field_id}", json=field_data.dict(exclude_none=True))

    def delete_custom_field(self, delete_data: "CommonDeleteDto", approve: str) -> None:
        """
        Delete custom fields.

        Args:
            delete_data: Data containing custom field IDs to delete
            approve: Approval confirmation (required)
        """
        if not approve:
            raise ValueError("Approval is required for deleting custom fields")

        self.client.delete("user-api/contacts/custom-fields", json=delete_data.dict(), params={"approve": approve})
