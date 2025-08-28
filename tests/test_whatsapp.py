from unittest.mock import Mock

import pytest

from devo_global_comms_python.exceptions import DevoValidationException
from devo_global_comms_python.resources.whatsapp import WhatsAppResource


class TestWhatsAppResource:
    """Test cases for the WhatsApp resource with new API implementation."""

    @pytest.fixture
    def whatsapp_resource(self, mock_client):
        """Create a WhatsApp resource instance."""
        return WhatsAppResource(mock_client)

    def test_get_accounts_success(self, whatsapp_resource):
        """Test getting WhatsApp accounts successfully."""
        # Setup mock response matching the API spec
        mock_response = Mock()
        mock_response.json.return_value = {
            "accounts": [
                {
                    "id": "acc_123",
                    "name": "Test Account",
                    "email": "test@example.com",
                    "phone": "+1234567890",
                    "is_approved": True,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z",
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 10,
            "has_next": False,
        }
        whatsapp_resource.client.get.return_value = mock_response

        # Test the get_accounts method
        result = whatsapp_resource.get_accounts(page=1, limit=10, is_approved=True)

        # Verify the request was made correctly
        whatsapp_resource.client.get.assert_called_once_with(
            "user-api/whatsapp/accounts",
            params={"page": 1, "limit": 10, "isApproved": True},
        )

        # Verify the response is correctly parsed
        assert len(result.accounts) == 1
        assert result.accounts[0].id == "acc_123"
        assert result.accounts[0].name == "Test Account"
        assert result.accounts[0].is_approved is True
        assert result.total == 1
        assert result.page == 1
        assert result.limit == 10
        assert result.has_next is False

    def test_get_accounts_with_search(self, whatsapp_resource):
        """Test getting WhatsApp accounts with search parameter."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "accounts": [],
            "total": 0,
            "page": 1,
            "limit": 10,
            "has_next": False,
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_accounts(search="test@example.com")

        whatsapp_resource.client.get.assert_called_once_with(
            "user-api/whatsapp/accounts",
            params={"search": "test@example.com"},
        )

        assert result.total == 0

    def test_get_accounts_no_params(self, whatsapp_resource):
        """Test getting WhatsApp accounts without any parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "accounts": [],
            "total": 0,
            "page": 1,
            "limit": 10,
            "has_next": False,
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_accounts()

        whatsapp_resource.client.get.assert_called_once_with(
            "user-api/whatsapp/accounts",
            params={},
        )

        assert result.total == 0

    def test_get_template_success(self, whatsapp_resource):
        """Test getting a WhatsApp template successfully."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "name": "welcome_message",
            "language": "en",
            "status": "APPROVED",
            "category": "MARKETING",
            "components": [
                {
                    "type": "BODY",
                    "text": "Welcome to our service, {{1}}!",
                    "parameters": [{"type": "TEXT"}],
                }
            ],
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_template("welcome_message")

        whatsapp_resource.client.get.assert_called_once_with("user-api/whatsapp/templates/welcome_message")

        assert result.name == "welcome_message"
        assert result.language == "en"
        assert result.status == "APPROVED"
        assert result.category == "MARKETING"
        assert len(result.components) == 1

    def test_get_template_missing_name(self, whatsapp_resource):
        """Test that missing template name raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            whatsapp_resource.get_template("")
        assert "name" in str(exc_info.value)

    def test_upload_file_success(self, whatsapp_resource):
        """Test uploading a file successfully."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "file_id": "file_123456",
            "filename": "document.pdf",
            "file_size": 1024,
            "mime_type": "application/pdf",
            "url": "https://example.com/files/file_123456",
            "expires_at": "2024-01-01T12:00:00Z",
        }
        whatsapp_resource.client.post.return_value = mock_response

        file_content = b"fake file content"
        result = whatsapp_resource.upload_file(file_content, "document.pdf", "application/pdf")

        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/upload",
            files={"file": ("document.pdf", file_content, "application/pdf")},
        )

        assert result.file_id == "file_123456"
        assert result.filename == "document.pdf"
        assert result.file_size == 1024
        assert result.mime_type == "application/pdf"
        assert result.url == "https://example.com/files/file_123456"

    def test_upload_file_missing_filename(self, whatsapp_resource):
        """Test that missing filename raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            whatsapp_resource.upload_file(b"content", "", "application/pdf")
        assert "filename" in str(exc_info.value)

    def test_upload_file_missing_content_type(self, whatsapp_resource):
        """Test that missing content type raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            whatsapp_resource.upload_file(b"content", "file.pdf", "")
        assert "content_type" in str(exc_info.value)

    def test_upload_file_empty_content(self, whatsapp_resource):
        """Test that empty file content raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            whatsapp_resource.upload_file(b"", "file.pdf", "application/pdf")
        assert "File content cannot be empty" in str(exc_info.value)

    def test_upload_file_with_image(self, whatsapp_resource):
        """Test uploading an image file."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "file_id": "img_789012",
            "filename": "image.jpg",
            "file_size": 2048,
            "mime_type": "image/jpeg",
            "url": "https://example.com/files/img_789012",
            "expires_at": "2024-01-01T12:00:00Z",
        }
        whatsapp_resource.client.post.return_value = mock_response

        fake_image = b"\xff\xd8\xff\xe0\x00\x10JFIF"  # Fake JPEG header
        result = whatsapp_resource.upload_file(fake_image, "image.jpg", "image/jpeg")

        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/upload",
            files={"file": ("image.jpg", fake_image, "image/jpeg")},
        )

        assert result.file_id == "img_789012"
        assert result.mime_type == "image/jpeg"

    def test_get_accounts_with_all_params(self, whatsapp_resource):
        """Test getting WhatsApp accounts with all parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "accounts": [
                {
                    "id": "acc_456",
                    "name": "Another Account",
                    "email": "another@example.com",
                    "phone": "+0987654321",
                    "is_approved": False,
                    "created_at": "2024-01-02T12:00:00Z",
                    "updated_at": "2024-01-02T12:00:00Z",
                }
            ],
            "total": 5,
            "page": 2,
            "limit": 5,
            "has_next": True,
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_accounts(page=2, limit=5, is_approved=False, search="another")

        whatsapp_resource.client.get.assert_called_once_with(
            "user-api/whatsapp/accounts",
            params={
                "page": 2,
                "limit": 5,
                "isApproved": False,
                "search": "another",
            },
        )

        assert len(result.accounts) == 1
        assert result.accounts[0].is_approved is False
        assert result.page == 2
        assert result.has_next is True

    def test_get_template_special_characters(self, whatsapp_resource):
        """Test getting a template with special characters in name."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "name": "special_template_123",
            "language": "es",
            "status": "APPROVED",
            "category": "UTILITY",
            "components": [],
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_template("special_template_123")

        whatsapp_resource.client.get.assert_called_once_with("user-api/whatsapp/templates/special_template_123")

        assert result.name == "special_template_123"
        assert result.language == "es"

    def test_upload_file_various_types(self, whatsapp_resource):
        """Test uploading different file types."""
        test_cases = [
            ("document.pdf", "application/pdf"),
            ("video.mp4", "video/mp4"),
            ("audio.mp3", "audio/mpeg"),
            ("image.png", "image/png"),
        ]

        for filename, content_type in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = {
                "file_id": f"file_{filename.split('.')[0]}",
                "filename": filename,
                "file_size": 1024,
                "mime_type": content_type,
                "url": f"https://example.com/files/{filename}",
                "expires_at": "2024-01-01T12:00:00Z",
            }
            whatsapp_resource.client.post.return_value = mock_response

            result = whatsapp_resource.upload_file(b"fake content", filename, content_type)

            assert result.filename == filename
            assert result.mime_type == content_type

    def test_send_normal_message_success(self, whatsapp_resource):
        """Test sending a normal WhatsApp message successfully."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_123456",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_normal_message(
            to="+1234567890", message="Hello from WhatsApp!", account_id="acc_123"
        )

        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/send-normal-message",
            json={
                "to": "+1234567890",
                "message": "Hello from WhatsApp!",
                "account_id": "acc_123",
            },
        )

        assert result.message_id == "msg_123456"
        assert result.status == "sent"
        assert result.to == "+1234567890"
        assert result.account_id == "acc_123"
        assert result.success is True

    def test_send_normal_message_without_account_id(self, whatsapp_resource):
        """Test sending a normal WhatsApp message without account_id."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_789012",
            "status": "sent",
            "to": "+0987654321",
            "account_id": "default_acc",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_normal_message(to="+0987654321", message="Hello without account ID!")

        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/send-normal-message",
            json={
                "to": "+0987654321",
                "message": "Hello without account ID!",
            },
        )

        assert result.message_id == "msg_789012"
        assert result.account_id == "default_acc"

    def test_send_normal_message_invalid_phone(self, whatsapp_resource):
        """Test that invalid phone number raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            whatsapp_resource.send_normal_message(to="invalid-phone", message="Hello!")
        assert "phone" in str(exc_info.value) or "to" in str(exc_info.value)

    def test_send_normal_message_empty_message(self, whatsapp_resource):
        """Test that empty message raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            whatsapp_resource.send_normal_message(to="+1234567890", message="")
        assert "message" in str(exc_info.value)

    def test_send_normal_message_long_content(self, whatsapp_resource):
        """Test sending a long WhatsApp message."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_long_123",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        long_message = "A" * 1000  # Long message
        result = whatsapp_resource.send_normal_message(to="+1234567890", message=long_message, account_id="acc_123")

        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/send-normal-message",
            json={
                "to": "+1234567890",
                "message": long_message,
                "account_id": "acc_123",
            },
        )

        assert result.success is True

    def test_send_normal_message_unicode_content(self, whatsapp_resource):
        """Test sending a WhatsApp message with Unicode content."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_unicode_123",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        unicode_message = "Hello 🌍! مرحبا بالعالم 你好世界"
        result = whatsapp_resource.send_normal_message(to="+1234567890", message=unicode_message, account_id="acc_123")

        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/send-normal-message",
            json={
                "to": "+1234567890",
                "message": unicode_message,
                "account_id": "acc_123",
            },
        )

        assert result.success is True

    def test_send_normal_message_api_error(self, whatsapp_resource):
        """Test handling API errors when sending message."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "",
            "status": "failed",
            "to": "+1234567890",
            "account_id": "acc_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": False,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_normal_message(to="+1234567890", message="Hello!", account_id="acc_123")

        assert result.success is False
        assert result.status == "failed"

    # Template Tests
    def test_create_template_authentication_success(self, whatsapp_resource):
        """Test creating an authentication template successfully."""
        from devo_global_comms_python.models.whatsapp import (
            BodyComponent,
            ButtonsComponent,
            FooterComponent,
            OTPButton,
            WhatsAppTemplateRequest,
        )

        # Create authentication template request
        template_request = WhatsAppTemplateRequest(
            name="authentication_code_copy_code_button",
            language="en_US",
            category="AUTHENTICATION",
            components=[
                BodyComponent(type="BODY", add_security_recommendation=True),
                FooterComponent(type="FOOTER", code_expiration_minutes=10),
                ButtonsComponent(
                    type="BUTTONS", buttons=[OTPButton(type="OTP", otp_type="COPY_CODE", text="Copy Code")]
                ),
            ],
        )

        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "template_123",
            "name": "authentication_code_copy_code_button",
            "language": "en_US",
            "category": "AUTHENTICATION",
            "status": "PENDING",
            "components": [],
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z",
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.create_template(account_id="acc_123", template=template_request)

        # Verify API call
        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/templates",
            params={"account_id": "acc_123"},
            json={
                "name": "authentication_code_copy_code_button",
                "language": "en_US",
                "category": "AUTHENTICATION",
                "components": [
                    {"type": "BODY", "add_security_recommendation": True},
                    {"type": "FOOTER", "code_expiration_minutes": 10},
                    {"type": "BUTTONS", "buttons": [{"type": "OTP", "otp_type": "COPY_CODE", "text": "Copy Code"}]},
                ],
            },
        )

        assert result.id == "template_123"
        assert result.name == "authentication_code_copy_code_button"
        assert result.category == "AUTHENTICATION"

    def test_create_template_marketing_with_buttons(self, whatsapp_resource):
        """Test creating a marketing template with various button types."""
        from devo_global_comms_python.models.whatsapp import (
            BodyComponent,
            ButtonsComponent,
            FooterComponent,
            HeaderComponent,
            PhoneNumberButton,
            TemplateExample,
            URLButton,
            WhatsAppTemplateRequest,
        )

        # Create marketing template with complex structure
        template_request = WhatsAppTemplateRequest(
            name="limited_time_offer",
            language="en_US",
            category="MARKETING",
            components=[
                HeaderComponent(type="HEADER", format="IMAGE", example=TemplateExample(header_handle=["4::aW..."])),
                BodyComponent(
                    type="BODY",
                    text="Hi {{1}}! For a limited time only you can get our {{2}} for as low as {{3}}.",
                    example=TemplateExample(body_text=[["Mark", "Tuscan Getaway package", "800"]]),
                ),
                FooterComponent(type="FOOTER", text="Offer valid until May 31, 2023"),
                ButtonsComponent(
                    type="BUTTONS",
                    buttons=[
                        PhoneNumberButton(type="PHONE_NUMBER", text="Call", phone_number="15550051310"),
                        URLButton(
                            type="URL",
                            text="Shop Now",
                            url="https://www.examplesite.com/shop?promo={{1}}",
                            example=["summer2023"],
                        ),
                    ],
                ),
            ],
        )

        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "template_456",
            "name": "limited_time_offer",
            "language": "en_US",
            "category": "MARKETING",
            "status": "APPROVED",
            "components": [],
            "created_at": "2024-01-01T12:00:00Z",
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.create_template(account_id="acc_456", template=template_request)

        assert result.id == "template_456"
        assert result.status == "APPROVED"

    def test_create_template_missing_account_id(self, whatsapp_resource):
        """Test template creation with missing account_id."""
        from devo_global_comms_python.models.whatsapp import BodyComponent, WhatsAppTemplateRequest

        template_request = WhatsAppTemplateRequest(
            name="test_template",
            language="en_US",
            category="UTILITY",
            components=[BodyComponent(type="BODY", text="Test message")],
        )

        with pytest.raises(DevoValidationException, match="account_id is required"):
            whatsapp_resource.create_template(account_id="", template=template_request)

    def test_get_templates_success(self, whatsapp_resource):
        """Test getting templates successfully."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "templates": [
                {
                    "name": "welcome_message",
                    "language": "en_US",
                    "status": "APPROVED",
                    "category": "UTILITY",
                    "components": [],
                    "created_at": "2024-01-01T12:00:00Z",
                },
                {
                    "name": "promotional_offer",
                    "language": "en_US",
                    "status": "PENDING",
                    "category": "MARKETING",
                    "components": [],
                    "created_at": "2024-01-01T11:00:00Z",
                },
            ],
            "total": 2,
            "page": 1,
            "limit": 10,
            "has_next": False,
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_templates(account_id="acc_123", page=1, limit=10, category="MARKETING")

        # Verify API call
        whatsapp_resource.client.get.assert_called_once_with(
            "user-api/whatsapp/templates", params={"id": "acc_123", "page": 1, "limit": 10, "category": "MARKETING"}
        )

        assert len(result.templates) == 2
        assert result.total == 2
        assert result.page == 1
        assert result.has_next is False

    def test_get_templates_with_search(self, whatsapp_resource):
        """Test getting templates with search parameter."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "templates": [
                {
                    "name": "welcome_message",
                    "language": "en_US",
                    "status": "APPROVED",
                    "category": "UTILITY",
                    "components": [],
                }
            ],
            "total": 1,
            "page": 1,
            "limit": 10,
            "has_next": False,
        }
        whatsapp_resource.client.get.return_value = mock_response

        result = whatsapp_resource.get_templates(account_id="acc_123", search="welcome")

        whatsapp_resource.client.get.assert_called_once_with(
            "user-api/whatsapp/templates", params={"id": "acc_123", "search": "welcome"}
        )

        assert len(result.templates) == 1
        assert result.templates[0].name == "welcome_message"

    def test_get_templates_invalid_category(self, whatsapp_resource):
        """Test templates retrieval with invalid category."""
        with pytest.raises(DevoValidationException, match="Invalid category"):
            whatsapp_resource.get_templates(account_id="acc_123", category="INVALID_CATEGORY")

    def test_get_templates_missing_account_id(self, whatsapp_resource):
        """Test templates retrieval with missing account_id."""
        with pytest.raises(DevoValidationException, match="account_id is required"):
            whatsapp_resource.get_templates(account_id="")

    def test_create_template_utility_with_location(self, whatsapp_resource):
        """Test creating a utility template with location header."""
        from devo_global_comms_python.models.whatsapp import (
            BodyComponent,
            ButtonsComponent,
            FooterComponent,
            HeaderComponent,
            QuickReplyButton,
            TemplateExample,
            WhatsAppTemplateRequest,
        )

        template_request = WhatsAppTemplateRequest(
            name="order_delivery_update",
            language="en_US",
            category="UTILITY",
            components=[
                HeaderComponent(type="HEADER", format="LOCATION"),
                BodyComponent(
                    type="BODY",
                    text="Good news {{1}}! Your order #{{2}} is on its way to the location above.",
                    example=TemplateExample(body_text=[["Mark", "566701"]]),
                ),
                FooterComponent(type="FOOTER", text="To stop receiving delivery updates, tap the button below."),
                ButtonsComponent(
                    type="BUTTONS", buttons=[QuickReplyButton(type="QUICK_REPLY", text="Stop Delivery Updates")]
                ),
            ],
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "template_789",
            "name": "order_delivery_update",
            "language": "en_US",
            "category": "UTILITY",
            "status": "APPROVED",
            "components": [],
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.create_template(account_id="acc_789", template=template_request)

        assert result.id == "template_789"
        assert result.category == "UTILITY"

    def test_create_template_with_catalog_button(self, whatsapp_resource):
        """Test creating template with catalog button."""
        from devo_global_comms_python.models.whatsapp import (
            BodyComponent,
            ButtonsComponent,
            CatalogButton,
            FooterComponent,
            TemplateExample,
            WhatsAppTemplateRequest,
        )

        template_request = WhatsAppTemplateRequest(
            name="intro_catalog_offer",
            language="en_US",
            category="MARKETING",
            components=[
                BodyComponent(
                    type="BODY",
                    text="Now shop for your favourite products right here on WhatsApp! "
                    "Get Rs {{1}} off on all orders above {{2}}Rs!",
                    example=TemplateExample(body_text=[["100", "400", "3"]]),
                ),
                FooterComponent(type="FOOTER", text="Best grocery deals on WhatsApp!"),
                ButtonsComponent(type="BUTTONS", buttons=[CatalogButton(type="CATALOG", text="View catalog")]),
            ],
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "template_catalog",
            "name": "intro_catalog_offer",
            "language": "en_US",
            "category": "MARKETING",
            "status": "PENDING",
            "components": [],
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.create_template(account_id="acc_catalog", template=template_request)

        assert result.id == "template_catalog"
        assert result.name == "intro_catalog_offer"

    # Template Message Sending Tests
    def test_send_template_message_authentication_success(self, whatsapp_resource):
        """Test sending an authentication template message."""
        from devo_global_comms_python.models.whatsapp import (
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        # Create authentication template message
        template_request = WhatsAppTemplateMessageRequest(
            to="905447423184",
            template=TemplateMessageTemplate(
                name="devotel_otp",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="body", parameters=[TemplateMessageParameter(type="text", text="123456")]
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="url",
                        index="0",
                        parameters=[TemplateMessageParameter(type="text", text="123456")],
                    ),
                ],
            ),
        )

        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_auth_123",
            "status": "sent",
            "to": "905447423184",
            "account_id": "acc_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_template_message(account_id="acc_123", template_message=template_request)

        # Verify API call
        whatsapp_resource.client.post.assert_called_once_with(
            "user-api/whatsapp/send-message-by-template",
            params={"account_id": "acc_123"},
            json={
                "messaging_product": "whatsapp",
                "to": "905447423184",
                "type": "template",
                "template": {
                    "name": "devotel_otp",
                    "language": {"code": "en_US"},
                    "components": [
                        {"type": "body", "parameters": [{"type": "text", "text": "123456"}]},
                        {
                            "type": "button",
                            "sub_type": "url",
                            "index": "0",
                            "parameters": [{"type": "text", "text": "123456"}],
                        },
                    ],
                },
            },
        )

        assert result.message_id == "msg_auth_123"
        assert result.success is True

    def test_send_template_message_with_image_header(self, whatsapp_resource):
        """Test sending template message with image header."""
        from devo_global_comms_python.models.whatsapp import (
            ImageParameter,
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="limited_time_offer_tuscan_getaway_2023",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="header",
                        parameters=[
                            TemplateMessageParameter(
                                type="image", image=ImageParameter(link="https://example.com/image.jpg")
                            )
                        ],
                    ),
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="Mark"),
                            TemplateMessageParameter(type="text", text="Tuscan Getaway package"),
                            TemplateMessageParameter(type="text", text="800"),
                        ],
                    ),
                ],
            ),
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_image_456",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_456",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_template_message(account_id="acc_456", template_message=template_request)

        assert result.message_id == "msg_image_456"
        assert result.success is True

    def test_send_template_message_with_location(self, whatsapp_resource):
        """Test sending template message with location parameter."""
        from devo_global_comms_python.models.whatsapp import (
            LocationParameter,
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="order_delivery_update",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="header",
                        parameters=[
                            TemplateMessageParameter(
                                type="location",
                                location=LocationParameter(
                                    latitude="37.7749",
                                    longitude="-122.4194",
                                    name="Delivery Location",
                                    address="San Francisco, CA",
                                ),
                            )
                        ],
                    ),
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="Mark"),
                            TemplateMessageParameter(type="text", text="566701"),
                        ],
                    ),
                ],
            ),
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_location_789",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_789",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_template_message(account_id="acc_789", template_message=template_request)

        assert result.message_id == "msg_location_789"

    def test_send_template_message_with_document(self, whatsapp_resource):
        """Test sending template message with document parameter."""
        from devo_global_comms_python.models.whatsapp import (
            DocumentParameter,
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="order_confirmation",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="header",
                        parameters=[
                            TemplateMessageParameter(
                                type="document",
                                document=DocumentParameter(
                                    link="https://example.com/receipt.pdf", filename="OrderReceipt.pdf"
                                ),
                            )
                        ],
                    ),
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="Mark"),
                            TemplateMessageParameter(type="text", text="860198-230332"),
                        ],
                    ),
                ],
            ),
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_doc_101112",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_101112",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_template_message(account_id="acc_101112", template_message=template_request)

        assert result.message_id == "msg_doc_101112"

    def test_send_template_message_with_buttons_payload(self, whatsapp_resource):
        """Test sending template message with button payload parameters."""
        from devo_global_comms_python.models.whatsapp import (
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="seasonal_promotion_text_only",
                language=TemplateMessageLanguage(code="en"),
                components=[
                    TemplateMessageComponent(
                        type="header", parameters=[TemplateMessageParameter(type="text", text="Summer Sale")]
                    ),
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="the end of August"),
                            TemplateMessageParameter(type="text", text="25OFF"),
                            TemplateMessageParameter(type="text", text="25%"),
                        ],
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="quick_reply",
                        index="0",
                        parameters=[TemplateMessageParameter(type="payload", payload="UNSUBSCRIBE_PROMOS")],
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="quick_reply",
                        index="1",
                        parameters=[TemplateMessageParameter(type="payload", payload="UNSUBSCRIBE_ALL")],
                    ),
                ],
            ),
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_buttons_131415",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_131415",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_template_message(account_id="acc_131415", template_message=template_request)

        assert result.message_id == "msg_buttons_131415"

    def test_send_template_message_missing_account_id(self, whatsapp_resource):
        """Test template message sending with missing account_id."""
        from devo_global_comms_python.models.whatsapp import (
            TemplateMessageLanguage,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(name="test_template", language=TemplateMessageLanguage(code="en_US")),
        )

        with pytest.raises(DevoValidationException, match="account_id is required"):
            whatsapp_resource.send_template_message(account_id="", template_message=template_request)

    def test_send_template_message_catalog_offer(self, whatsapp_resource):
        """Test sending catalog offer template message."""
        from devo_global_comms_python.models.whatsapp import (
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="intro_catalog_offer",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="100"),
                            TemplateMessageParameter(type="text", text="400"),
                            TemplateMessageParameter(type="text", text="3"),
                        ],
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="url",
                        index="0",
                        parameters=[
                            TemplateMessageParameter(type="text", text="View Catalog"),
                            TemplateMessageParameter(type="payload", payload="CATALOG_URL"),
                        ],
                    ),
                ],
            ),
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "message_id": "msg_catalog_161718",
            "status": "sent",
            "to": "+1234567890",
            "account_id": "acc_161718",
            "timestamp": "2024-01-01T12:00:00Z",
            "success": True,
        }
        whatsapp_resource.client.post.return_value = mock_response

        result = whatsapp_resource.send_template_message(account_id="acc_161718", template_message=template_request)

        assert result.message_id == "msg_catalog_161718"
        assert result.success is True
