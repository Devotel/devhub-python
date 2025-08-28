from unittest.mock import Mock, patch

import pytest

from devo_global_comms_python.client import DevoClient
from devo_global_comms_python.exceptions import DevoInvalidPhoneNumberException, DevoValidationException
from devo_global_comms_python.models.rcs import (
    RcsAccountSerializer,
    RCSMessage,
    RcsSendMessageSerializer,
    SuccessSerializer,
)


@pytest.fixture
def rcs_client():
    """Create a mock RCS client for testing."""
    return DevoClient(api_key="test_api_key")


class TestRCSAccountManagement:
    """Test RCS account management endpoints."""

    def test_create_account(self, rcs_client):
        """Test creating an RCS account."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "acc_123",
            "name": "Test Account",
            "brand_name": "Test Brand",
            "business_description": "Test business description",
            "contact_email": "test@example.com",
            "contact_phone": "+1234567890",
            "website_url": "https://example.com",
            "logo_url": "https://example.com/logo.png",
            "privacy_policy_url": "https://example.com/privacy",
            "terms_of_service_url": "https://example.com/terms",
            "is_approved": False,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }

        with patch.object(rcs_client, "post", return_value=mock_response):
            account_data = {
                "name": "Test Account",
                "brand_name": "Test Brand",
                "business_description": "Test business description",
                "contact_email": "test@example.com",
                "contact_phone": "+1234567890",
                "website_url": "https://example.com",
                "logo_url": "https://example.com/logo.png",
            }
            result = rcs_client.rcs.create_account(account_data)

            assert isinstance(result, RcsAccountSerializer)
            assert result.id == "acc_123"
            assert result.name == "Test Account"
            assert result.brand_name == "Test Brand"
            assert result.is_approved is False

    def test_get_accounts(self, rcs_client):
        """Test getting RCS accounts."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "acc_123",
                "name": "Test Account 1",
                "brand_name": "Test Brand 1",
                "business_description": "Description 1",
                "contact_email": "test1@example.com",
                "contact_phone": "+1234567890",
                "is_approved": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
            {
                "id": "acc_456",
                "name": "Test Account 2",
                "brand_name": "Test Brand 2",
                "business_description": "Description 2",
                "contact_email": "test2@example.com",
                "contact_phone": "+1234567891",
                "is_approved": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
        ]

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.get_accounts(page=1, limit=10, is_approved="true")

            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(account, RcsAccountSerializer) for account in result)
            assert result[0].id == "acc_123"
            assert result[1].id == "acc_456"

    def test_verify_account(self, rcs_client):
        """Test verifying an RCS account."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "message": "Account verified successfully",
            "data": {"account_id": "acc_123"},
        }

        with patch.object(rcs_client, "post", return_value=mock_response):
            verification_data = {"account_id": "acc_123", "verification_code": "123456"}
            result = rcs_client.rcs.verify_account(verification_data)

            assert isinstance(result, SuccessSerializer)
            assert result.success is True
            assert result.message == "Account verified successfully"

    def test_update_account(self, rcs_client):
        """Test updating an RCS account."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}

        with patch.object(rcs_client, "put", return_value=mock_response):
            update_data = {"name": "Updated Account Name"}
            result = rcs_client.rcs.update_account("acc_123", update_data)

            assert result == {"success": True}

    def test_get_account_details(self, rcs_client):
        """Test getting account details."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "acc_123", "name": "Test Account", "details": "Account details"}

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.get_account_details("acc_123")

            assert result["id"] == "acc_123"
            assert result["name"] == "Test Account"


class TestRCSMessaging:
    """Test RCS messaging endpoints."""

    def test_send_message(self, rcs_client):
        """Test sending an RCS message."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_123",
            "account_id": "acc_123",
            "to": "+1234567890",
            "from": "+0987654321",
            "message_type": "text",
            "status": "sent",
            "direction": "outbound",
            "text": "Hello, this is a test message",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }

        with patch.object(rcs_client, "post", return_value=mock_response):
            message_data = {
                "to": "+1234567890",
                "account_id": "acc_123",
                "message_type": "text",
                "text": "Hello, this is a test message",
            }
            result = rcs_client.rcs.send_message(message_data)

            assert isinstance(result, RcsSendMessageSerializer)
            assert result.id == "msg_123"
            assert result.to == "+1234567890"
            assert result.message_type == "text"
            assert result.status == "sent"

    def test_send_rich_card_message(self, rcs_client):
        """Test sending a rich card RCS message."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_456",
            "account_id": "acc_123",
            "to": "+1234567890",
            "message_type": "rich_card",
            "status": "sent",
            "direction": "outbound",
            "rich_card": {
                "title": "Rich Card Title",
                "description": "Rich card description",
                "media_url": "https://example.com/image.jpg",
            },
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }

        with patch.object(rcs_client, "post", return_value=mock_response):
            message_data = {
                "to": "+1234567890",
                "account_id": "acc_123",
                "message_type": "rich_card",
                "rich_card": {
                    "title": "Rich Card Title",
                    "description": "Rich card description",
                    "media_url": "https://example.com/image.jpg",
                },
            }
            result = rcs_client.rcs.send_message(message_data)

            assert isinstance(result, RcsSendMessageSerializer)
            assert result.id == "msg_456"
            assert result.message_type == "rich_card"
            assert result.rich_card["title"] == "Rich Card Title"

    def test_list_messages(self, rcs_client):
        """Test listing RCS messages."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "msg_123",
                "account_id": "acc_123",
                "to": "+1234567890",
                "message_type": "text",
                "status": "delivered",
                "direction": "outbound",
                "text": "Message 1",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
            {
                "id": "msg_456",
                "account_id": "acc_123",
                "to": "+1234567891",
                "message_type": "rich_card",
                "status": "sent",
                "direction": "outbound",
                "rich_card": {"title": "Card Title"},
                "created_at": "2024-01-01T01:00:00Z",
                "updated_at": "2024-01-01T01:00:00Z",
            },
        ]

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.list_messages(page=1, limit=10, type="text")

            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(msg, RcsSendMessageSerializer) for msg in result)
            assert result[0].id == "msg_123"
            assert result[1].id == "msg_456"


class TestRCSTemplateManagement:
    """Test RCS template management endpoints."""

    def test_create_template(self, rcs_client):
        """Test creating an RCS template."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "template_id": "tmpl_123"}

        with patch.object(rcs_client, "post", return_value=mock_response):
            template_data = {
                "name": "Test Template",
                "title": "Template Title",
                "description": "Template description",
                "content": {"text": "Hello {{name}}"},
                "category": "marketing",
                "account_id": "acc_123",
            }
            result = rcs_client.rcs.create_template(template_data)

            assert result["success"] is True
            assert result["template_id"] == "tmpl_123"

    def test_get_templates(self, rcs_client):
        """Test getting RCS templates."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "tmpl_123",
                "name": "Template 1",
                "title": "Title 1",
                "description": "Description 1",
                "content": {"text": "Content 1"},
                "category": "marketing",
                "account_id": "acc_123",
                "status": "approved",
            },
            {
                "id": "tmpl_456",
                "name": "Template 2",
                "title": "Title 2",
                "description": "Description 2",
                "content": {"text": "Content 2"},
                "category": "utility",
                "account_id": "acc_123",
                "status": "pending",
            },
        ]

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.get_templates(page=1, limit=10)

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == "tmpl_123"
            assert result[1]["id"] == "tmpl_456"

    def test_delete_template(self, rcs_client):
        """Test deleting RCS templates."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "deleted_count": 2}

        with patch.object(rcs_client, "delete", return_value=mock_response):
            delete_data = {"ids": ["tmpl_123", "tmpl_456"], "reason": "No longer needed"}
            result = rcs_client.rcs.delete_template(delete_data, approve="true")

            assert result["success"] is True
            assert result["deleted_count"] == 2

    def test_update_template(self, rcs_client):
        """Test updating an RCS template."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}

        with patch.object(rcs_client, "put", return_value=mock_response):
            update_data = {"title": "Updated Template Title", "description": "Updated description"}
            result = rcs_client.rcs.update_template("tmpl_123", update_data)

            assert result["success"] is True


class TestRCSBrandManagement:
    """Test RCS brand management endpoints."""

    def test_get_brands(self, rcs_client):
        """Test getting RCS brands."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "brand_123",
                "name": "Brand 1",
                "description": "Brand description 1",
                "logo_url": "https://example.com/logo1.png",
                "primary_color": "#FF0000",
                "account_id": "acc_123",
            },
            {
                "id": "brand_456",
                "name": "Brand 2",
                "description": "Brand description 2",
                "logo_url": "https://example.com/logo2.png",
                "primary_color": "#00FF00",
                "account_id": "acc_123",
            },
        ]

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.get_brands(page=1, limit=10, search="Brand")

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == "brand_123"
            assert result[1]["id"] == "brand_456"

    def test_create_brand(self, rcs_client):
        """Test creating an RCS brand."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "brand_id": "brand_789"}

        with patch.object(rcs_client, "post", return_value=mock_response):
            brand_data = {
                "name": "New Brand",
                "description": "New brand description",
                "logo_url": "https://example.com/new-logo.png",
                "primary_color": "#0000FF",
                "account_id": "acc_123",
            }
            result = rcs_client.rcs.create_brand(brand_data)

            assert result["success"] is True
            assert result["brand_id"] == "brand_789"

    def test_update_brand(self, rcs_client):
        """Test updating an RCS brand."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}

        with patch.object(rcs_client, "put", return_value=mock_response):
            update_data = {"name": "Updated Brand Name", "description": "Updated brand description"}
            result = rcs_client.rcs.update_brand("brand_123", update_data)

            assert result["success"] is True


class TestRCSTesterManagement:
    """Test RCS tester management endpoints."""

    def test_add_tester(self, rcs_client):
        """Test adding an RCS tester."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "tester_id": "tester_123"}

        with patch.object(rcs_client, "post", return_value=mock_response):
            tester_data = {
                "phone_number": "+1234567890",
                "name": "Test Tester",
                "email": "tester@example.com",
                "account_id": "acc_123",
            }
            result = rcs_client.rcs.add_tester(tester_data)

            assert result["success"] is True
            assert result["tester_id"] == "tester_123"

    def test_get_testers(self, rcs_client):
        """Test getting RCS testers."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": "tester_123",
                "phone_number": "+1234567890",
                "name": "Tester 1",
                "email": "tester1@example.com",
                "account_id": "acc_123",
                "status": "active",
            },
            {
                "id": "tester_456",
                "phone_number": "+1234567891",
                "name": "Tester 2",
                "email": "tester2@example.com",
                "account_id": "acc_123",
                "status": "inactive",
            },
        ]

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.get_testers(account_id="acc_123", page=1, limit=10, search="Tester")

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == "tester_123"
            assert result[1]["id"] == "tester_456"


class TestRCSLegacyMethods:
    """Test legacy RCS methods for backward compatibility."""

    def test_send_text_legacy(self, rcs_client):
        """Test legacy send_text method."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_legacy_123",
            "to": "+1234567890",
            "type": "text",
            "text": "Legacy text message",
            "status": "sent",
            "direction": "outbound",
            "date_created": "2024-01-01T00:00:00Z",
        }

        with patch.object(rcs_client, "post", return_value=mock_response):
            result = rcs_client.rcs.send_text(
                to="+1234567890", text="Legacy text message", callback_url="https://example.com/callback"
            )

            assert isinstance(result, RCSMessage)
            assert result.id == "msg_legacy_123"
            assert result.text == "Legacy text message"

    def test_send_rich_card_legacy(self, rcs_client):
        """Test legacy send_rich_card method."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_legacy_456",
            "to": "+1234567890",
            "type": "rich_card",
            "rich_card": {
                "title": "Legacy Rich Card",
                "description": "Legacy description",
                "media_url": "https://example.com/legacy.jpg",
            },
            "status": "sent",
            "direction": "outbound",
            "date_created": "2024-01-01T00:00:00Z",
        }

        with patch.object(rcs_client, "post", return_value=mock_response):
            result = rcs_client.rcs.send_rich_card(
                to="+1234567890",
                title="Legacy Rich Card",
                description="Legacy description",
                media_url="https://example.com/legacy.jpg",
            )

            assert isinstance(result, RCSMessage)
            assert result.id == "msg_legacy_456"
            assert result.rich_card["title"] == "Legacy Rich Card"

    def test_get_legacy(self, rcs_client):
        """Test legacy get method."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_legacy_789",
            "to": "+1234567890",
            "type": "text",
            "text": "Retrieved message",
            "status": "delivered",
            "direction": "outbound",
            "date_created": "2024-01-01T00:00:00Z",
        }

        with patch.object(rcs_client, "get", return_value=mock_response):
            result = rcs_client.rcs.get("msg_legacy_789")

            assert isinstance(result, RCSMessage)
            assert result.id == "msg_legacy_789"
            assert result.text == "Retrieved message"


class TestRCSValidation:
    """Test RCS validation and error handling."""

    def test_invalid_account_id_validation(self, rcs_client):
        """Test validation of account ID."""
        with pytest.raises(DevoValidationException, match="account_id is required"):
            rcs_client.rcs.update_account("", {"name": "Test"})

    def test_invalid_template_id_validation(self, rcs_client):
        """Test validation of template ID."""
        with pytest.raises(DevoValidationException, match="template_id is required"):
            rcs_client.rcs.update_template("", {"title": "Test"})

    def test_invalid_brand_id_validation(self, rcs_client):
        """Test validation of brand ID."""
        with pytest.raises(DevoValidationException, match="brand_id is required"):
            rcs_client.rcs.update_brand("", {"name": "Test"})

    def test_invalid_message_id_validation(self, rcs_client):
        """Test validation of message ID for legacy method."""
        with pytest.raises(DevoValidationException, match="message_id is required"):
            rcs_client.rcs.get("")

    def test_phone_number_validation(self, rcs_client):
        """Test phone number validation in legacy methods."""
        with pytest.raises(DevoInvalidPhoneNumberException):
            rcs_client.rcs.send_text("invalid_phone", "Test message")

    def test_required_account_id_for_testers(self, rcs_client):
        """Test required account_id parameter for get_testers."""
        with pytest.raises(DevoValidationException, match="account_id is required"):
            rcs_client.rcs.get_testers("")
