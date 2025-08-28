from datetime import datetime
from unittest.mock import Mock

import pytest

from devo_global_comms_python.models.messages import SendMessageDto, SendMessageSerializer
from devo_global_comms_python.resources.messages import MessagesResource


class TestMessagesResource:
    """Test cases for the MessagesResource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.messages_resource = MessagesResource(self.mock_client)

    def test_send_sms_message(self):
        """Test sending an SMS message through omni-channel endpoint."""
        # Arrange
        send_data = SendMessageDto(channel="sms", to="+1234567890", payload={"text": "Hello World"})

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_123",
            "channel": "sms",
            "to": "+1234567890",
            "from": "+0987654321",
            "status": "sent",
            "direction": "outbound",
            "content": {"text": "Hello World"},
            "created_at": "2024-01-01T12:00:00Z",
        }
        self.mock_client.post.return_value = mock_response

        # Act
        result = self.messages_resource.send(send_data)

        # Assert
        assert isinstance(result, SendMessageSerializer)
        assert result.id == "msg_123"
        assert result.channel == "sms"
        assert result.to == "+1234567890"
        assert result.status == "sent"
        assert result.content == {"text": "Hello World"}

        self.mock_client.post.assert_called_once_with(
            "messages/send", data={"channel": "sms", "to": "+1234567890", "payload": {"text": "Hello World"}}
        )

    def test_send_email_message(self):
        """Test sending an email message through omni-channel endpoint."""
        # Arrange
        send_data = SendMessageDto(
            channel="email",
            to="user@example.com",
            **{"from": "sender@example.com"},
            payload={"subject": "Test Email", "text": "Hello World", "html": "<h1>Hello World</h1>"},
            callback_url="https://example.com/webhook",
            metadata={"campaign": "test"},
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "email_456",
            "channel": "email",
            "to": "user@example.com",
            "from": "sender@example.com",
            "status": "queued",
            "direction": "outbound",
            "content": {"subject": "Test Email", "text": "Hello World", "html": "<h1>Hello World</h1>"},
            "created_at": "2024-01-01T12:00:00Z",
            "metadata": {"campaign": "test"},
        }
        self.mock_client.post.return_value = mock_response

        # Act
        result = self.messages_resource.send(send_data)

        # Assert
        assert isinstance(result, SendMessageSerializer)
        assert result.id == "email_456"
        assert result.channel == "email"
        assert result.to == "user@example.com"
        assert result.from_ == "sender@example.com"
        assert result.status == "queued"
        assert result.metadata == {"campaign": "test"}

        self.mock_client.post.assert_called_once_with(
            "messages/send",
            data={
                "channel": "email",
                "to": "user@example.com",
                "from": "sender@example.com",
                "payload": {"subject": "Test Email", "text": "Hello World", "html": "<h1>Hello World</h1>"},
                "callback_url": "https://example.com/webhook",
                "metadata": {"campaign": "test"},
            },
        )

    def test_send_whatsapp_message(self):
        """Test sending a WhatsApp message through omni-channel endpoint."""
        # Arrange
        send_data = SendMessageDto(
            channel="whatsapp", to="+1234567890", payload={"type": "text", "text": {"body": "Hello World"}}
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "wa_789",
            "channel": "whatsapp",
            "to": "+1234567890",
            "status": "sent",
            "direction": "outbound",
            "content": {"type": "text", "text": {"body": "Hello World"}},
            "created_at": "2024-01-01T12:00:00Z",
        }
        self.mock_client.post.return_value = mock_response

        # Act
        result = self.messages_resource.send(send_data)

        # Assert
        assert isinstance(result, SendMessageSerializer)
        assert result.id == "wa_789"
        assert result.channel == "whatsapp"
        assert result.to == "+1234567890"
        assert result.status == "sent"

        self.mock_client.post.assert_called_once_with(
            "messages/send",
            data={
                "channel": "whatsapp",
                "to": "+1234567890",
                "payload": {"type": "text", "text": {"body": "Hello World"}},
            },
        )

    def test_send_rcs_message(self):
        """Test sending an RCS message through omni-channel endpoint."""
        # Arrange
        send_data = SendMessageDto(
            channel="rcs",
            to="+1234567890",
            payload={"message_type": "text", "text": "Hello World", "agent_id": "agent_123"},
        )

        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "rcs_abc",
            "channel": "rcs",
            "to": "+1234567890",
            "status": "sent",
            "direction": "outbound",
            "content": {"message_type": "text", "text": "Hello World", "agent_id": "agent_123"},
            "created_at": "2024-01-01T12:00:00Z",
        }
        self.mock_client.post.return_value = mock_response

        # Act
        result = self.messages_resource.send(send_data)

        # Assert
        assert isinstance(result, SendMessageSerializer)
        assert result.id == "rcs_abc"
        assert result.channel == "rcs"
        assert result.to == "+1234567890"
        assert result.status == "sent"

        self.mock_client.post.assert_called_once_with(
            "messages/send",
            data={
                "channel": "rcs",
                "to": "+1234567890",
                "payload": {"message_type": "text", "text": "Hello World", "agent_id": "agent_123"},
            },
        )

    def test_send_message_with_validation_error(self):
        """Test send message with invalid channel."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            SendMessageDto(
                channel="invalid_channel", to="+1234567890", payload={"text": "Hello World"}  # Invalid channel
            )

    def test_send_message_api_error(self):
        """Test send message when API returns error."""
        # Arrange
        send_data = SendMessageDto(channel="sms", to="+1234567890", payload={"text": "Hello World"})

        self.mock_client.post.side_effect = Exception("API Error")

        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            self.messages_resource.send(send_data)

    def test_send_message_dto_alias_handling(self):
        """Test that SendMessageDto properly handles the 'from' field alias."""
        # Arrange
        send_data = SendMessageDto(
            channel="sms",
            to="+1234567890",
            **{"from": "+0987654321"},  # Use from as keyword argument
            payload={"text": "Hello World"},
        )

        # Act
        data_dict = send_data.model_dump(by_alias=True, exclude_none=True)

        # Assert
        assert "from" in data_dict
        assert "from_" not in data_dict
        assert data_dict["from"] == "+0987654321"

    def test_send_message_serializer_datetime_parsing(self):
        """Test that SendMessageSerializer properly parses datetime fields."""
        # Arrange
        data = {
            "id": "msg_123",
            "channel": "sms",
            "to": "+1234567890",
            "status": "sent",
            "direction": "outbound",
            "content": {"text": "Hello World"},
            "created_at": "2024-01-01T12:00:00Z",
        }

        # Act
        serializer = SendMessageSerializer(**data)

        # Assert
        assert isinstance(serializer.created_at, datetime)
        assert serializer.created_at.year == 2024
        assert serializer.created_at.month == 1
        assert serializer.created_at.day == 1


class TestSendMessageDto:
    """Test cases for SendMessageDto model."""

    def test_valid_sms_payload(self):
        """Test creating valid SMS payload."""
        dto = SendMessageDto(channel="sms", to="+1234567890", payload={"text": "Hello World"})

        assert dto.channel == "sms"
        assert dto.to == "+1234567890"
        assert dto.payload == {"text": "Hello World"}

    def test_valid_email_payload(self):
        """Test creating valid email payload."""
        dto = SendMessageDto(
            channel="email", to="user@example.com", payload={"subject": "Test", "text": "Hello", "html": "<p>Hello</p>"}
        )

        assert dto.channel == "email"
        assert dto.to == "user@example.com"
        assert dto.payload["subject"] == "Test"

    def test_invalid_channel(self):
        """Test that invalid channel raises validation error."""
        with pytest.raises(ValueError):
            SendMessageDto(channel="invalid", to="+1234567890", payload={"text": "Hello"})

    def test_optional_fields(self):
        """Test optional fields are handled correctly."""
        dto = SendMessageDto(
            channel="sms",
            to="+1234567890",
            **{"from": "+0987654321"},  # Use from as keyword argument
            payload={"text": "Hello"},
            callback_url="https://example.com/webhook",
            metadata={"key": "value"},
        )

        assert dto.from_ == "+0987654321"
        assert dto.callback_url == "https://example.com/webhook"
        assert dto.metadata == {"key": "value"}


class TestSendMessageSerializer:
    """Test cases for SendMessageSerializer model."""

    def test_basic_serialization(self):
        """Test basic serialization of response data."""
        data = {
            "id": "msg_123",
            "channel": "sms",
            "to": "+1234567890",
            "status": "sent",
            "direction": "outbound",
            "content": {"text": "Hello World"},
            "created_at": "2024-01-01T12:00:00Z",
        }

        serializer = SendMessageSerializer(**data)

        assert serializer.id == "msg_123"
        assert serializer.channel == "sms"
        assert serializer.to == "+1234567890"
        assert serializer.status == "sent"
        assert serializer.direction == "outbound"
        assert serializer.content == {"text": "Hello World"}

    def test_optional_fields_serialization(self):
        """Test serialization with optional fields."""
        data = {
            "id": "msg_123",
            "channel": "email",
            "to": "user@example.com",
            "from": "sender@example.com",
            "status": "delivered",
            "direction": "outbound",
            "content": {"subject": "Test", "text": "Hello"},
            "pricing": {"cost": 0.01, "currency": "USD"},
            "created_at": "2024-01-01T12:00:00Z",
            "metadata": {"campaign": "test"},
        }

        serializer = SendMessageSerializer(**data)

        assert serializer.from_ == "sender@example.com"
        assert serializer.pricing == {"cost": 0.01, "currency": "USD"}
        assert serializer.metadata == {"campaign": "test"}
