from unittest.mock import Mock, patch

import pytest

from devo_global_comms_python.exceptions import DevoValidationException
from devo_global_comms_python.resources.sms import SMSResource


class TestSMSResource:
    """Test cases for the SMS resource."""

    @pytest.fixture
    def sms_resource(self, mock_client):
        """Create an SMS resource instance."""
        return SMSResource(mock_client)

    def test_send_sms_success(self, sms_resource, test_phone_number):
        """Test sending an SMS successfully."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "sid": "SMS123456789",
            "to": test_phone_number,
            "body": "Hello, World!",
            "status": "queued",
        }
        sms_resource.client.post.return_value = mock_response

        with patch("devo_global_comms_python.models.sms.SMSMessage") as mock_model:
            mock_model.parse_obj.return_value = Mock(sid="SMS123456789")

            result = sms_resource.send(to=test_phone_number, body="Hello, World!")

            assert result.sid == "SMS123456789"
            sms_resource.client.post.assert_called_once()

    def test_send_sms_with_invalid_phone_number(self, sms_resource):
        """Test sending SMS with invalid phone number."""
        with pytest.raises(DevoValidationException):
            sms_resource.send(to="invalid-phone", body="Hello, World!")

    def test_send_sms_with_empty_body(self, sms_resource, test_phone_number):
        """Test sending SMS with empty body."""
        with pytest.raises(DevoValidationException):
            sms_resource.send(to=test_phone_number, body="")

    def test_send_sms_with_optional_params(self, sms_resource, test_phone_number):
        """Test sending SMS with optional parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {"sid": "SMS123456789"}
        sms_resource.client.post.return_value = mock_response

        with patch("devo_global_comms_python.models.sms.SMSMessage") as mock_model:
            mock_model.parse_obj.return_value = Mock(sid="SMS123456789")

            sms_resource.send(
                to=test_phone_number,
                body="Hello, World!",
                from_="+1987654321",
                callback_url="https://example.com/webhook",
                metadata={"campaign": "test"},
            )

            # Verify the request was made with correct data
            call_args = sms_resource.client.post.call_args
            assert call_args[0][0] == "sms/messages"
            assert "from" in call_args[1]["json"]
            assert "callback_url" in call_args[1]["json"]
            assert "metadata" in call_args[1]["json"]

    def test_get_sms_message(self, sms_resource):
        """Test retrieving an SMS message."""
        message_sid = "SMS123456789"
        mock_response = Mock()
        mock_response.json.return_value = {"sid": message_sid}
        sms_resource.client.get.return_value = mock_response

        with patch("devo_global_comms_python.models.sms.SMSMessage") as mock_model:
            mock_model.parse_obj.return_value = Mock(sid=message_sid)

            result = sms_resource.get(message_sid)

            assert result.sid == message_sid
            sms_resource.client.get.assert_called_with(f"sms/messages/{message_sid}")

    def test_list_sms_messages(self, sms_resource):
        """Test listing SMS messages."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "messages": [
                {"sid": "SMS1", "body": "Message 1"},
                {"sid": "SMS2", "body": "Message 2"},
            ]
        }
        sms_resource.client.get.return_value = mock_response

        with patch("devo_global_comms_python.models.sms.SMSMessage") as mock_model:
            mock_model.parse_obj.side_effect = [Mock(sid="SMS1"), Mock(sid="SMS2")]

            result = sms_resource.list(limit=10, offset=0)

            assert len(result) == 2
            sms_resource.client.get.assert_called_with(
                "sms/messages", params={"limit": 10, "offset": 0}
            )

    def test_list_sms_messages_with_filters(self, sms_resource, test_phone_number):
        """Test listing SMS messages with filters."""
        mock_response = Mock()
        mock_response.json.return_value = {"messages": []}
        sms_resource.client.get.return_value = mock_response

        with patch("devo_global_comms_python.models.sms.SMSMessage"):
            sms_resource.list(
                to=test_phone_number, status="delivered", date_sent_after="2024-01-01"
            )

            call_args = sms_resource.client.get.call_args
            params = call_args[1]["params"]
            assert params["to"] == test_phone_number
            assert params["status"] == "delivered"
            assert params["date_sent_after"] == "2024-01-01"

    def test_cancel_sms_message(self, sms_resource):
        """Test canceling an SMS message."""
        message_sid = "SMS123456789"
        mock_response = Mock()
        mock_response.json.return_value = {"sid": message_sid, "status": "canceled"}
        sms_resource.client.delete.return_value = mock_response

        with patch("devo_global_comms_python.models.sms.SMSMessage") as mock_model:
            mock_model.parse_obj.return_value = Mock(sid=message_sid, status="canceled")

            result = sms_resource.cancel(message_sid)

            assert result.sid == message_sid
            assert result.status == "canceled"
            sms_resource.client.delete.assert_called_with(f"sms/messages/{message_sid}")
