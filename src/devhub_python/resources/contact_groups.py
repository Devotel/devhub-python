from typing import TYPE_CHECKING, List, Optional

from ..utils import validate_required_string, validate_response
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.contact_groups import (
        ContactsGroup,
        ContactsGroupListResponse,
        CreateContactsGroupDto,
        DeleteContactsGroupsDto,
        UpdateContactsGroupDto,
    )


class ContactGroupsResource(BaseResource):
    """
    Contact Groups Resource for managing contact group operations.

    This resource provides methods to create, read, update and delete contact groups,
    as well as bulk operations for managing multiple groups.
    """

    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
    ) -> "ContactsGroupListResponse":
        """
        Get contact groups by user ID with pagination and search.

        Args:
            page: Page number for pagination
            limit: Number of items per page
            search: Search term to filter groups
            search_fields: Fields to search in

        Returns:
            ContactsGroupListResponse with groups and pagination info

        Example:
            groups = client.contact_groups.list(page=1, limit=10, search="marketing")
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if search:
            params["search"] = search
        if search_fields:
            params["search_fields"] = search_fields

        response = self.client.get("contacts-groups", params=params)

        from ..models.contact_groups import ContactsGroupListResponse

        return validate_response(response, ContactsGroupListResponse)

    def create(self, data: "CreateContactsGroupDto") -> "ContactsGroup":
        """
        Create a new contact group.

        Args:
            data: CreateContactsGroupDto with group details

        Returns:
            ContactsGroup: The created contact group

        Example:
            from ..models.contact_groups import CreateContactsGroupDto

            group_data = CreateContactsGroupDto(
                name="Marketing List",
                description="Contacts for marketing campaigns",
                contact_ids=["contact_1", "contact_2"]
            )
            group = client.contact_groups.create(group_data)
        """
        response = self.client.post("contacts-groups", data=data.model_dump(exclude_none=True))

        from ..models.contact_groups import ContactsGroup

        return validate_response(response, ContactsGroup)

    def update(self, group_id: str, data: "UpdateContactsGroupDto") -> "ContactsGroup":
        """
        Update an existing contact group.

        Args:
            group_id: ID of the contact group to update
            data: UpdateContactsGroupDto with updated details

        Returns:
            ContactsGroup: The updated contact group

        Example:
            from ..models.contact_groups import UpdateContactsGroupDto

            update_data = UpdateContactsGroupDto(
                name="Updated Marketing List",
                description="Updated description"
            )
            group = client.contact_groups.update("group_123", update_data)
        """
        group_id = validate_required_string(group_id, "group_id")
        response = self.client.put(f"contacts-groups/{group_id}", data=data.model_dump(exclude_none=True))

        from ..models.contact_groups import ContactsGroup

        return validate_response(response, ContactsGroup)

    def delete_by_id(self, group_id: str, approve: Optional[str] = None) -> "ContactsGroup":
        """
        Delete a single contact group by ID.

        Args:
            group_id: ID of the contact group to delete
            approve: Approval confirmation for deletion

        Returns:
            ContactsGroup: The deleted contact group details

        Example:
            deleted_group = client.contact_groups.delete_by_id("group_123", approve="yes")
        """
        group_id = validate_required_string(group_id, "group_id")
        params = {}
        if approve:
            params["approve"] = approve

        response = self.client.delete(f"contacts-groups/{group_id}", params=params)

        from ..models.contact_groups import ContactsGroup

        return validate_response(response, ContactsGroup)

    def delete_bulk(self, data: "DeleteContactsGroupsDto", approve: Optional[str] = None) -> "ContactsGroup":
        """
        Delete multiple contact groups in bulk.

        Args:
            data: DeleteContactsGroupsDto with group IDs to delete
            approve: Approval confirmation for deletion

        Returns:
            ContactsGroup: Details of the bulk deletion operation

        Example:
            from ..models.contact_groups import DeleteContactsGroupsDto

            delete_data = DeleteContactsGroupsDto(
                group_ids=["group_1", "group_2", "group_3"],
                transfer_contacts_to="group_backup"
            )
            result = client.contact_groups.delete_bulk(delete_data, approve="yes")
        """
        params = {}
        if approve:
            params["approve"] = approve

        response = self.client.delete(
            "contacts-groups",
            params=params,
            data=data.model_dump(exclude_none=True),
        )

        from ..models.contact_groups import ContactsGroup

        return validate_response(response, ContactsGroup)

    def get_by_id(self, group_id: str) -> "ContactsGroup":
        """
        Get a specific contact group by ID.

        Note: This method assumes the existence of a GET endpoint for individual groups,
        which is common but not explicitly defined in the provided API spec.

        Args:
            group_id: ID of the contact group to retrieve

        Returns:
            ContactsGroup: The contact group details

        Example:
            group = client.contact_groups.get_by_id("group_123")
        """
        group_id = validate_required_string(group_id, "group_id")
        response = self.client.get(f"contacts-groups/{group_id}")

        from ..models.contact_groups import ContactsGroup

        return validate_response(response, ContactsGroup)

    def search(
        self,
        query: str,
        fields: Optional[List[str]] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> "ContactsGroupListResponse":
        """
        Search contact groups with specific criteria.

        Args:
            query: Search query string
            fields: Fields to search in (name, description, etc.)
            page: Page number for pagination
            limit: Number of items per page

        Returns:
            ContactsGroupListResponse with matching groups

        Example:
            results = client.contact_groups.search(
                query="marketing",
                fields=["name", "description"],
                page=1,
                limit=20
            )
        """
        return self.list(page=page, limit=limit, search=query, search_fields=fields)
