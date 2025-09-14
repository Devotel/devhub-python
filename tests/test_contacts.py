from unittest.mock import Mock

import pytest

from devhub_python import DevoClient
from devhub_python.exceptions import DevoValidationException
from devhub_python.models.contacts import (
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
from devhub_python.resources.contacts import ContactsResource


class TestContactsResource:
    """Test cases for the ContactsResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = DevoClient(api_key="test_api_key")
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.put = Mock()
        self.client.delete = Mock()
        self.client.patch = Mock()
        self.contacts_resource = ContactsResource(self.client)

    def test_list_contacts(self):
        """Test listing contacts with basic parameters."""
        # Mock response data
        mock_response_data = {
            "contacts": [
                {
                    "id": "contact_1",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone_number": "+1234567890",
                    "created_at": "2023-01-01T00:00:00Z",
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 50,
            "total_pages": 1,
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.get.return_value = mock_response

        # Test the method
        result = self.contacts_resource.list(page=1, limit=50)

        # Assertions
        self.client.get.assert_called_once_with("user-api/contacts", params={"page": 1, "limit": 50})
        assert isinstance(result, GetContactsSerializer)
        assert result.total == 1
        assert len(result.contacts) == 1
        assert result.contacts[0].first_name == "John"

    def test_list_contacts_with_filters(self):
        """Test listing contacts with advanced filters."""
        mock_response_data = {
            "contacts": [
                {
                    "id": "contact_1",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane.smith@example.com",
                    "is_email_subscribed": True,
                    "tags": ["vip", "customer"],
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 10,
            "total_pages": 1,
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.get.return_value = mock_response

        # Test with filters
        result = self.contacts_resource.list(
            page=1,
            limit=10,
            search="jane",
            search_fields=["first_name", "last_name"],
            is_email_subscribed=True,
            tags=["vip"],
            country_codes=["US"],
        )

        # Check parameters
        expected_params = {
            "page": 1,
            "limit": 10,
            "search": "jane",
            "search_fields": ["first_name", "last_name"],
            "is_email_subscribed": True,
            "tags": ["vip"],
            "country_codes": ["US"],
        }

        self.client.get.assert_called_once_with("user-api/contacts", params=expected_params)
        assert isinstance(result, GetContactsSerializer)

    def test_create_contact(self):
        """Test creating a new contact."""
        # Mock response data
        mock_response_data = {
            "id": "new_contact_id",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@example.com",
            "phone_number": "+1987654321",
            "is_email_subscribed": True,
            "created_at": "2023-01-02T00:00:00Z",
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.post.return_value = mock_response

        # Create test data
        contact_data = CreateContactDto(
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            phone_number="+1987654321",
            is_email_subscribed=True,
            tags=["customer"],
            metadata={"source": "api_test"},
        )

        # Test the method
        result = self.contacts_resource.create(contact_data)

        # Assertions
        self.client.post.assert_called_once_with("user-api/contacts", json=contact_data.dict(exclude_none=True))
        assert isinstance(result, ContactSerializer)
        assert result.first_name == "Alice"
        assert result.email == "alice.johnson@example.com"

    def test_update_contact(self):
        """Test updating an existing contact."""
        contact_id = "contact_123"
        mock_response_data = {
            "id": contact_id,
            "first_name": "Alice Updated",
            "last_name": "Johnson",
            "email": "alice.updated@example.com",
            "updated_at": "2023-01-03T00:00:00Z",
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.put.return_value = mock_response

        # Create update data
        update_data = UpdateContactDto(
            first_name="Alice Updated", email="alice.updated@example.com", tags=["vip", "customer"]
        )

        # Test the method
        result = self.contacts_resource.update(contact_id, update_data)

        # Assertions
        self.client.put.assert_called_once_with(
            f"user-api/contacts/{contact_id}", json=update_data.dict(exclude_none=True)
        )
        assert isinstance(result, ContactSerializer)
        assert result.first_name == "Alice Updated"

    def test_delete_bulk_contacts(self):
        """Test bulk deletion of contacts."""
        mock_response_data = {"id": "delete_operation_id", "status": "completed"}

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.delete.return_value = mock_response

        # Create delete data
        delete_data = DeleteContactsDto(contact_ids=["contact_1", "contact_2", "contact_3"])

        # Test the method
        result = self.contacts_resource.delete_bulk(delete_data, approve="yes")

        # Assertions
        self.client.delete.assert_called_once_with(
            "user-api/contacts", json=delete_data.dict(), params={"approve": "yes"}
        )
        assert isinstance(result, ContactSerializer)

    def test_assign_to_group(self):
        """Test assigning contacts to a group."""
        assignment_data = AssignToContactsGroupDto(
            contact_ids=["contact_1", "contact_2"], contacts_group_id="group_123"
        )

        # Test the method
        self.contacts_resource.assign_to_group(assignment_data)

        # Assertions
        self.client.patch.assert_called_once_with("user-api/contacts/assign-to-group", json=assignment_data.dict())

    def test_unassign_from_group(self):
        """Test unassigning contacts from a group."""
        assignment_data = AssignToContactsGroupDto(
            contact_ids=["contact_1", "contact_2"], contacts_group_id="group_123"
        )

        # Test the method
        self.contacts_resource.unassign_from_group(assignment_data)

        # Assertions
        self.client.patch.assert_called_once_with("user-api/contacts/unassign-from-group", json=assignment_data.dict())

    def test_import_from_csv(self):
        """Test importing contacts from CSV."""
        mock_response_data = {
            "total_processed": 100,
            "successfully_created": 95,
            "skipped_duplicates": 3,
            "failed_imports": 2,
            "errors": ["Invalid email format on row 15", "Missing phone number on row 87"],
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.post.return_value = mock_response

        # Create CSV import data
        csv_data = CreateContactsFromCsvDto(
            csv_data="first_name,last_name,email\nJohn,Doe,john@example.com\nJane,Smith,jane@example.com",
            contacts_group_id="group_123",
            skip_duplicates=True,
        )

        # Test the method
        result = self.contacts_resource.import_from_csv(csv_data, approve="yes")

        # Assertions
        self.client.post.assert_called_once_with(
            "user-api/contacts/csv", json=csv_data.dict(), params={"approve": "yes"}
        )
        assert isinstance(result, CreateContactsFromCsvRespDto)
        assert result.total_processed == 100
        assert result.successfully_created == 95

    # Custom Fields Tests

    def test_list_custom_fields(self):
        """Test listing custom fields."""
        mock_response_data = {
            "custom_fields": [
                {
                    "id": "field_1",
                    "name": "Customer Level",
                    "field_type": "select",
                    "options": ["Bronze", "Silver", "Gold"],
                    "created_at": "2023-01-01T00:00:00Z",
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 50,
            "total_pages": 1,
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.get.return_value = mock_response

        # Test the method
        result = self.contacts_resource.list_custom_fields(page=1, limit=50)

        # Assertions
        self.client.get.assert_called_once_with("user-api/contacts/custom-fields", params={"page": 1, "limit": 50})
        assert isinstance(result, GetCustomFieldsSerializer)
        assert result.total == 1
        assert len(result.custom_fields) == 1

    def test_create_custom_field(self):
        """Test creating a custom field."""
        mock_response_data = {
            "id": "new_field_id",
            "name": "Department",
            "field_type": "text",
            "description": "Employee department",
            "is_required": False,
            "created_at": "2023-01-02T00:00:00Z",
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        self.client.post.return_value = mock_response

        # Create field data
        field_data = CreateCustomFieldDto(
            name="Department", field_type="text", description="Employee department", is_required=False
        )

        # Test the method
        result = self.contacts_resource.create_custom_field(field_data)

        # Assertions
        self.client.post.assert_called_once_with("user-api/contacts/custom-fields", json=field_data.dict())
        assert isinstance(result, CustomFieldSerializer)
        assert result.name == "Department"

    def test_update_custom_field(self):
        """Test updating a custom field."""
        field_id = "field_123"
        field_data = UpdateCustomFieldDto(description="Updated description", is_required=True)

        # Test the method
        self.contacts_resource.update_custom_field(field_id, field_data)

        # Assertions
        self.client.put.assert_called_once_with(
            f"user-api/contacts/custom-fields/{field_id}", json=field_data.dict(exclude_none=True)
        )

    def test_delete_custom_field(self):
        """Test deleting custom fields."""
        delete_data = CommonDeleteDto(ids=["field_1", "field_2"])

        # Test the method
        self.contacts_resource.delete_custom_field(delete_data, approve="yes")

        # Assertions
        self.client.delete.assert_called_once_with(
            "user-api/contacts/custom-fields", json=delete_data.dict(), params={"approve": "yes"}
        )

    def test_delete_custom_field_without_approval(self):
        """Test that deleting custom fields requires approval."""
        delete_data = CommonDeleteDto(ids=["field_1"])

        # Test the method should raise ValueError
        with pytest.raises(ValueError, match="Approval is required"):
            self.contacts_resource.delete_custom_field(delete_data, approve="")

    def test_validation_error_empty_contact_id(self):
        """Test validation error for empty contact ID."""
        update_data = UpdateContactDto(first_name="Test")

        with pytest.raises(DevoValidationException, match="contact_id is required and cannot be empty"):
            self.contacts_resource.update("", update_data)


class TestCreateContactDto:
    """Test cases for CreateContactDto validation."""

    def test_valid_create_dto(self):
        """Test creating a valid contact DTO."""
        dto = CreateContactDto(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            tags=["customer", "vip"],
            metadata={"source": "website"},
        )

        assert dto.first_name == "John"
        assert dto.email == "john.doe@example.com"
        assert dto.phone_number == "+1234567890"
        assert "customer" in dto.tags

    def test_email_validation(self):
        """Test email validation."""
        with pytest.raises(ValueError, match="Invalid email format"):
            CreateContactDto(email="invalid-email")

    def test_phone_validation(self):
        """Test phone number validation."""
        with pytest.raises(ValueError, match="must be in E.164 format"):
            CreateContactDto(phone_number="1234567890")  # Missing +


class TestUpdateContactDto:
    """Test cases for UpdateContactDto validation."""

    def test_valid_update_dto(self):
        """Test creating a valid update DTO."""
        dto = UpdateContactDto(first_name="Jane", tags=["updated"])

        assert dto.first_name == "Jane"
        assert "updated" in dto.tags

    def test_email_validation(self):
        """Test email validation in update DTO."""
        with pytest.raises(ValueError, match="Invalid email format"):
            UpdateContactDto(email="invalid-email")


class TestDeleteContactsDto:
    """Test cases for DeleteContactsDto validation."""

    def test_valid_delete_dto(self):
        """Test creating a valid delete DTO."""
        dto = DeleteContactsDto(contact_ids=["contact_1", "contact_2"])

        assert len(dto.contact_ids) == 2
        assert "contact_1" in dto.contact_ids

    def test_empty_contact_ids(self):
        """Test validation for empty contact IDs."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            DeleteContactsDto(contact_ids=[])


class TestAssignToContactsGroupDto:
    """Test cases for AssignToContactsGroupDto validation."""

    def test_valid_assignment_dto(self):
        """Test creating a valid assignment DTO."""
        dto = AssignToContactsGroupDto(contact_ids=["contact_1", "contact_2"], contacts_group_id="group_123")

        assert len(dto.contact_ids) == 2
        assert dto.contacts_group_id == "group_123"

    def test_empty_contact_ids(self):
        """Test validation for empty contact IDs."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            AssignToContactsGroupDto(contact_ids=[], contacts_group_id="group_123")

    def test_empty_group_id(self):
        """Test validation for empty group ID."""
        with pytest.raises(ValueError, match="Contact group ID cannot be empty"):
            AssignToContactsGroupDto(contact_ids=["contact_1"], contacts_group_id="")


class TestCreateCustomFieldDto:
    """Test cases for CreateCustomFieldDto validation."""

    def test_valid_custom_field_dto(self):
        """Test creating a valid custom field DTO."""
        dto = CreateCustomFieldDto(
            name="Customer Level", field_type="select", options=["Bronze", "Silver", "Gold"], is_required=True
        )

        assert dto.name == "Customer Level"
        assert dto.field_type == "select"
        assert len(dto.options) == 3

    def test_empty_name(self):
        """Test validation for empty field name."""
        with pytest.raises(ValueError, match="Custom field name cannot be empty"):
            CreateCustomFieldDto(name="", field_type="text")

    def test_invalid_field_type(self):
        """Test validation for invalid field type."""
        with pytest.raises(ValueError, match="Field type must be one of"):
            CreateCustomFieldDto(name="Test Field", field_type="invalid_type")


class TestServicesNamespaceContacts:
    """Test cases for contacts integration with services namespace."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = DevoClient(api_key="test_api_key")

    def test_contacts_available_via_services(self):
        """Test that contacts resource is available via services namespace."""
        assert hasattr(self.client.services, "contacts")
        assert self.client.services.contacts is not None
        assert isinstance(self.client.services.contacts, ContactsResource)

    def test_services_namespace_string_representation_includes_contacts(self):
        """Test that services namespace includes contacts functionality."""
        services_repr = repr(self.client.services)
        assert "ServicesNamespace" in services_repr
        # Ensure contacts resource is properly initialized
        assert hasattr(self.client.services, "contacts")
