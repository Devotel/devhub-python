from datetime import datetime
from unittest.mock import Mock

import pytest

from src.devo_global_comms_python.models.contact_groups import (
    ContactsGroup,
    ContactsGroupListResponse,
    CreateContactsGroupDto,
    DeleteContactsGroupsDto,
    UpdateContactsGroupDto,
)
from src.devo_global_comms_python.resources.contact_groups import ContactGroupsResource


class TestContactGroupsResource:
    """Test cases for the ContactGroupsResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.contact_groups_resource = ContactGroupsResource(self.mock_client)

    def test_list_contact_groups(self):
        """Test listing contact groups with pagination."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "groups": [
                {
                    "id": "group_1",
                    "name": "Marketing List",
                    "description": "Marketing contacts",
                    "contacts_count": 150,
                    "created_at": "2024-01-01T12:00:00Z",
                    "user_id": "user_123",
                },
                {
                    "id": "group_2",
                    "name": "Sales Team",
                    "description": "Sales contacts",
                    "contacts_count": 75,
                    "created_at": "2024-01-02T12:00:00Z",
                    "user_id": "user_123",
                },
            ],
            "total": 25,
            "page": 1,
            "limit": 10,
            "total_pages": 3,
        }
        self.mock_client.get.return_value = mock_response

        # Act
        result = self.contact_groups_resource.list(page=1, limit=10, search="marketing")

        # Assert
        assert isinstance(result, ContactsGroupListResponse)
        assert len(result.groups) == 2
        assert result.total == 25
        assert result.page == 1
        assert result.limit == 10
        assert result.total_pages == 3
        assert result.groups[0].name == "Marketing List"

        self.mock_client.get.assert_called_once_with(
            "contacts-groups", params={"page": 1, "limit": 10, "search": "marketing"}
        )

    def test_list_contact_groups_with_search_fields(self):
        """Test listing contact groups with search fields."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "groups": [],
            "total": 0,
            "page": 1,
            "limit": 10,
            "total_pages": 0,
        }
        self.mock_client.get.return_value = mock_response

        # Act
        self.contact_groups_resource.list(search="test", search_fields=["name", "description"])

        # Assert
        self.mock_client.get.assert_called_once_with(
            "contacts-groups",
            params={"search": "test", "search_fields": ["name", "description"]},
        )

    def test_create_contact_group(self):
        """Test creating a new contact group."""
        # Arrange
        create_data = CreateContactsGroupDto(
            name="New Marketing List",
            description="A new marketing contact group",
            contact_ids=["contact_1", "contact_2", "contact_3"],
            metadata={"campaign": "summer_2024"},
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "group_new",
            "name": "New Marketing List",
            "description": "A new marketing contact group",
            "contacts_count": 3,
            "created_at": "2024-01-15T12:00:00Z",
            "user_id": "user_123",
            "metadata": {"campaign": "summer_2024"},
        }
        self.mock_client.post.return_value = mock_response

        # Act
        result = self.contact_groups_resource.create(create_data)

        # Assert
        assert isinstance(result, ContactsGroup)
        assert result.id == "group_new"
        assert result.name == "New Marketing List"
        assert result.description == "A new marketing contact group"
        assert result.contacts_count == 3
        assert result.metadata == {"campaign": "summer_2024"}

        self.mock_client.post.assert_called_once_with(
            "contacts-groups",
            data={
                "name": "New Marketing List",
                "description": "A new marketing contact group",
                "contact_ids": ["contact_1", "contact_2", "contact_3"],
                "metadata": {"campaign": "summer_2024"},
            },
        )

    def test_update_contact_group(self):
        """Test updating an existing contact group."""
        # Arrange
        update_data = UpdateContactsGroupDto(
            name="Updated Marketing List",
            description="Updated description",
            metadata={"updated": True},
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "group_123",
            "name": "Updated Marketing List",
            "description": "Updated description",
            "contacts_count": 150,
            "updated_at": "2024-01-15T14:00:00Z",
            "user_id": "user_123",
            "metadata": {"updated": True},
        }
        self.mock_client.put.return_value = mock_response

        # Act
        result = self.contact_groups_resource.update("group_123", update_data)

        # Assert
        assert isinstance(result, ContactsGroup)
        assert result.id == "group_123"
        assert result.name == "Updated Marketing List"
        assert result.description == "Updated description"
        assert result.metadata == {"updated": True}

        self.mock_client.put.assert_called_once_with(
            "contacts-groups/group_123",
            data={
                "name": "Updated Marketing List",
                "description": "Updated description",
                "metadata": {"updated": True},
            },
        )

    def test_delete_contact_group_by_id(self):
        """Test deleting a contact group by ID."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "group_123",
            "name": "Deleted Group",
            "description": "This group was deleted",
            "contacts_count": 0,
            "user_id": "user_123",
        }
        self.mock_client.delete.return_value = mock_response

        # Act
        result = self.contact_groups_resource.delete_by_id("group_123", approve="yes")

        # Assert
        assert isinstance(result, ContactsGroup)
        assert result.id == "group_123"
        assert result.name == "Deleted Group"

        self.mock_client.delete.assert_called_once_with("contacts-groups/group_123", params={"approve": "yes"})

    def test_delete_contact_group_by_id_without_approval(self):
        """Test deleting a contact group by ID without approval."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "group_123",
            "name": "Deleted Group",
            "description": "This group was deleted",
            "contacts_count": 0,
            "user_id": "user_123",
        }
        self.mock_client.delete.return_value = mock_response

        # Act
        result = self.contact_groups_resource.delete_by_id("group_123")

        # Assert
        assert isinstance(result, ContactsGroup)
        self.mock_client.delete.assert_called_once_with("contacts-groups/group_123", params={})

    def test_delete_contact_groups_bulk(self):
        """Test bulk deleting contact groups."""
        # Arrange
        delete_data = DeleteContactsGroupsDto(
            group_ids=["group_1", "group_2", "group_3"],
            transfer_contacts_to="group_backup",
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "bulk_delete_operation",
            "name": "Bulk Delete Operation",
            "description": "Deleted 3 groups",
            "contacts_count": 0,
            "user_id": "user_123",
        }
        self.mock_client.delete.return_value = mock_response

        # Act
        result = self.contact_groups_resource.delete_bulk(delete_data, approve="yes")

        # Assert
        assert isinstance(result, ContactsGroup)
        assert result.name == "Bulk Delete Operation"

        self.mock_client.delete.assert_called_once_with(
            "contacts-groups",
            params={"approve": "yes"},
            data={
                "group_ids": ["group_1", "group_2", "group_3"],
                "transfer_contacts_to": "group_backup",
            },
        )

    def test_get_contact_group_by_id(self):
        """Test getting a specific contact group by ID."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "group_123",
            "name": "Marketing List",
            "description": "Marketing contacts",
            "contacts_count": 150,
            "created_at": "2024-01-01T12:00:00Z",
            "user_id": "user_123",
        }
        self.mock_client.get.return_value = mock_response

        # Act
        result = self.contact_groups_resource.get_by_id("group_123")

        # Assert
        assert isinstance(result, ContactsGroup)
        assert result.id == "group_123"
        assert result.name == "Marketing List"
        assert result.contacts_count == 150

        self.mock_client.get.assert_called_once_with("contacts-groups/group_123")

    def test_search_contact_groups(self):
        """Test searching contact groups."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "groups": [
                {
                    "id": "group_1",
                    "name": "Marketing Team",
                    "description": "Marketing department contacts",
                    "contacts_count": 25,
                    "created_at": "2024-01-01T12:00:00Z",
                    "user_id": "user_123",
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 20,
            "total_pages": 1,
        }
        self.mock_client.get.return_value = mock_response

        # Act
        result = self.contact_groups_resource.search(
            query="marketing", fields=["name", "description"], page=1, limit=20
        )

        # Assert
        assert isinstance(result, ContactsGroupListResponse)
        assert len(result.groups) == 1
        assert result.groups[0].name == "Marketing Team"

        self.mock_client.get.assert_called_once_with(
            "contacts-groups",
            params={
                "page": 1,
                "limit": 20,
                "search": "marketing",
                "search_fields": ["name", "description"],
            },
        )

    def test_validation_error_empty_group_id(self):
        """Test validation error for empty group ID."""
        with pytest.raises(Exception):  # DevoValidationException would be raised
            self.contact_groups_resource.delete_by_id("")

    def test_api_error_handling(self):
        """Test API error handling."""
        # Arrange
        self.mock_client.get.side_effect = Exception("API Error")

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            self.contact_groups_resource.list()


class TestCreateContactsGroupDto:
    """Test cases for CreateContactsGroupDto model."""

    def test_valid_create_dto(self):
        """Test creating valid CreateContactsGroupDto."""
        dto = CreateContactsGroupDto(
            name="Test Group",
            description="A test group",
            contact_ids=["contact_1", "contact_2"],
            metadata={"test": True},
        )

        assert dto.name == "Test Group"
        assert dto.description == "A test group"
        assert dto.contact_ids == ["contact_1", "contact_2"]
        assert dto.metadata == {"test": True}

    def test_minimum_valid_create_dto(self):
        """Test creating CreateContactsGroupDto with minimum required fields."""
        dto = CreateContactsGroupDto(name="Minimum Group")

        assert dto.name == "Minimum Group"
        assert dto.description is None
        assert dto.contact_ids is None
        assert dto.metadata is None

    def test_invalid_empty_name(self):
        """Test validation error for empty name."""
        with pytest.raises(ValueError):
            CreateContactsGroupDto(name="")

    def test_invalid_long_name(self):
        """Test validation error for name that's too long."""
        with pytest.raises(ValueError):
            CreateContactsGroupDto(name="x" * 256)  # Over 255 characters

    def test_invalid_long_description(self):
        """Test validation error for description that's too long."""
        with pytest.raises(ValueError):
            CreateContactsGroupDto(name="Test Group", description="x" * 1001)  # Over 1000 characters


class TestUpdateContactsGroupDto:
    """Test cases for UpdateContactsGroupDto model."""

    def test_valid_update_dto(self):
        """Test creating valid UpdateContactsGroupDto."""
        dto = UpdateContactsGroupDto(
            name="Updated Group",
            description="Updated description",
            contact_ids=["contact_1"],
            metadata={"updated": True},
        )

        assert dto.name == "Updated Group"
        assert dto.description == "Updated description"
        assert dto.contact_ids == ["contact_1"]
        assert dto.metadata == {"updated": True}

    def test_partial_update_dto(self):
        """Test creating UpdateContactsGroupDto with partial fields."""
        dto = UpdateContactsGroupDto(name="Only Name Updated")

        assert dto.name == "Only Name Updated"
        assert dto.description is None
        assert dto.contact_ids is None
        assert dto.metadata is None

    def test_empty_update_dto(self):
        """Test creating empty UpdateContactsGroupDto."""
        dto = UpdateContactsGroupDto()

        assert dto.name is None
        assert dto.description is None
        assert dto.contact_ids is None
        assert dto.metadata is None


class TestDeleteContactsGroupsDto:
    """Test cases for DeleteContactsGroupsDto model."""

    def test_valid_delete_dto(self):
        """Test creating valid DeleteContactsGroupsDto."""
        dto = DeleteContactsGroupsDto(
            group_ids=["group_1", "group_2"],
            transfer_contacts_to="backup_group",
        )

        assert dto.group_ids == ["group_1", "group_2"]
        assert dto.transfer_contacts_to == "backup_group"

    def test_delete_dto_without_transfer(self):
        """Test creating DeleteContactsGroupsDto without transfer group."""
        dto = DeleteContactsGroupsDto(group_ids=["group_1", "group_2"])

        assert dto.group_ids == ["group_1", "group_2"]
        assert dto.transfer_contacts_to is None

    def test_invalid_empty_group_ids(self):
        """Test validation error for empty group_ids list."""
        with pytest.raises(ValueError):
            DeleteContactsGroupsDto(group_ids=[])


class TestContactsGroup:
    """Test cases for ContactsGroup model."""

    def test_valid_contacts_group(self):
        """Test creating valid ContactsGroup."""
        group = ContactsGroup(
            id="group_123",
            name="Test Group",
            description="A test group",
            contacts_count=50,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            user_id="user_123",
            metadata={"test": True},
        )

        assert group.id == "group_123"
        assert group.name == "Test Group"
        assert group.description == "A test group"
        assert group.contacts_count == 50
        assert group.user_id == "user_123"
        assert group.metadata == {"test": True}

    def test_minimum_valid_contacts_group(self):
        """Test creating ContactsGroup with minimum required fields."""
        group = ContactsGroup(id="group_123", name="Minimum Group")

        assert group.id == "group_123"
        assert group.name == "Minimum Group"
        assert group.description is None
        assert group.contacts_count is None
        assert group.created_at is None
        assert group.user_id is None
        assert group.metadata is None


class TestContactsGroupListResponse:
    """Test cases for ContactsGroupListResponse model."""

    def test_valid_list_response(self):
        """Test creating valid ContactsGroupListResponse."""
        groups = [
            ContactsGroup(id="group_1", name="Group 1"),
            ContactsGroup(id="group_2", name="Group 2"),
        ]

        response = ContactsGroupListResponse(groups=groups, total=25, page=1, limit=10, total_pages=3)

        assert len(response.groups) == 2
        assert response.total == 25
        assert response.page == 1
        assert response.limit == 10
        assert response.total_pages == 3

    def test_empty_list_response(self):
        """Test creating empty ContactsGroupListResponse."""
        response = ContactsGroupListResponse(groups=[], total=0, page=1, limit=10, total_pages=0)

        assert len(response.groups) == 0
        assert response.total == 0
        assert response.page == 1
        assert response.total_pages == 0
