from datetime import datetime
from unittest.mock import Mock

import pytest

from devo_global_comms_python.exceptions import DevoValidationException
from devo_global_comms_python.resources.sms import SMSResource


class TestSMSResource:
    """Test cases for the SMS resource with new API implementation."""

    @pytest.fixture
    def sms_resource(self, mock_client):
        """Create an SMS resource instance."""
        return SMSResource(mock_client)

    def test_send_sms_success(self, sms_resource, test_phone_number):
        """Test sending an SMS successfully using the new quick-send API."""
        # Setup mock response matching the API spec
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_123456789",
            "user_id": "user_123",
            "tenant_id": "tenant_123",
            "sender_id": "sender_123",
            "recipient": test_phone_number,
            "message": "Hello, World!",
            "account_id": "account_123",
            "account_type": "sms",
            "status": "queued",
            "message_timeline": {},
            "message_id": "msg_123456789",
            "bulksmsid": "bulk_123",
            "sent_date": "2024-01-01T12:00:00Z",
            "direction": "sent",
            "recipientcontactid": "contact_123",
            "api_route": "user-api/sms/quick-send",
            "apimode": "quick-send",
            "quicksendidentifier": "quick_123",
            "hirvalidation": True,
        }
        sms_resource.client.post.return_value = mock_response

        # Test the new send_sms method
        result = sms_resource.send_sms(
            recipient=test_phone_number,
            message="Hello, World!",
            sender="+1987654321",
            hirvalidation=True,
        )

        # Verify the response
        assert result.id == "msg_123456789"
        assert result.recipient == test_phone_number
        assert result.message == "Hello, World!"
        assert result.status == "queued"
        assert result.hirvalidation is True

        # Verify the API call
        sms_resource.client.post.assert_called_once_with(
            "user-api/sms/quick-send",
            json={
                "sender": "+1987654321",
                "recipient": test_phone_number,
                "message": "Hello, World!",
                "hirvalidation": True,
            },
        )

    def test_send_sms_with_invalid_recipient(self, sms_resource):
        """Test sending SMS with invalid recipient phone number."""
        with pytest.raises(DevoValidationException):
            sms_resource.send_sms(
                recipient="invalid-phone",
                message="Hello, World!",
                sender="+1987654321",
            )

    def test_send_sms_with_empty_message(self, sms_resource, test_phone_number):
        """Test sending SMS with empty message."""
        with pytest.raises(DevoValidationException):
            sms_resource.send_sms(recipient=test_phone_number, message="", sender="+1987654321")

    def test_send_sms_with_empty_sender(self, sms_resource, test_phone_number):
        """Test sending SMS with empty sender."""
        with pytest.raises(DevoValidationException):
            sms_resource.send_sms(recipient=test_phone_number, message="Hello, World!", sender="")

    def test_get_senders_success(self, sms_resource):
        """Test retrieving senders list successfully."""
        # Setup mock response matching the API spec
        mock_response = Mock()
        mock_response.json.return_value = {
            "senders": [
                {
                    "id": "sender_1",
                    "sender_id": "sender_123",
                    "gateways_id": "gateway_1",
                    "phone_number": "+1234567890",
                    "number": "+1234567890",
                    "istest": False,
                    "type": "number",
                },
                {
                    "id": "sender_2",
                    "sender_id": "sender_456",
                    "gateways_id": "gateway_2",
                    "phone_number": "+1987654321",
                    "number": "+1987654321",
                    "istest": True,
                    "type": "number",
                },
            ]
        }
        sms_resource.client.get.return_value = mock_response

        result = sms_resource.get_senders()

        # Verify the response
        assert len(result.senders) == 2
        assert result.senders[0].phone_number == "+1234567890"
        assert result.senders[0].istest is False
        assert result.senders[1].phone_number == "+1987654321"
        assert result.senders[1].istest is True

        # Verify the API call
        sms_resource.client.get.assert_called_once_with("user-api/me/senders")

    def test_buy_number_success(self, sms_resource):
        """Test purchasing a phone number successfully."""
        # Setup mock response matching the API spec
        mock_response = Mock()
        mock_response.json.return_value = {
            "features": [
                {
                    "name": "SMS",
                    "reservable": True,
                    "region_id": "US",
                    "number_type": "mobile",
                    "quickship": True,
                    "region_information": {
                        "region_type": "country",
                        "region_name": "United States",
                    },
                    "phone_number": "+1234567890",
                    "cost_information": {
                        "monthly_cost": "1.00",
                        "setup_cost": "0.00",
                        "currency": "USD",
                    },
                    "best_effort": False,
                    "number_provider_type": "twilio",
                }
            ]
        }
        sms_resource.client.post.return_value = mock_response

        result = sms_resource.buy_number(
            region="US",
            number="+1234567890",
            number_type="mobile",
            agency_authorized_representative="Jane Doe",
            agency_representative_email="jane.doe@company.com",
            is_longcode=True,
            is_automated_enabled=True,
        )

        # Verify the response
        assert len(result.features) == 1
        feature = result.features[0]
        assert feature.phone_number == "+1234567890"
        assert feature.region_information.region_name == "United States"
        assert feature.cost_information.monthly_cost == "1.00"

        # Verify the API call
        call_args = sms_resource.client.post.call_args
        assert call_args[0][0] == "user-api/numbers/buy"
        request_data = call_args[1]["json"]
        assert request_data["region"] == "US"
        assert request_data["number"] == "+1234567890"
        assert request_data["number_type"] == "mobile"
        assert request_data["agency_authorized_representative"] == "Jane Doe"
        assert request_data["agency_representative_email"] == "jane.doe@company.com"

    def test_buy_number_with_invalid_email(self, sms_resource):
        """Test purchasing a number with invalid email."""
        with pytest.raises(DevoValidationException):
            sms_resource.buy_number(
                region="US",
                number="+1234567890",
                number_type="mobile",
                agency_authorized_representative="Jane Doe",
                agency_representative_email="invalid-email",
            )

    def test_buy_number_with_datetime(self, sms_resource):
        """Test purchasing a number with agreement date."""
        mock_response = Mock()
        mock_response.json.return_value = {"features": []}
        sms_resource.client.post.return_value = mock_response

        agreement_date = datetime(2024, 1, 1, 12, 0, 0)

        sms_resource.buy_number(
            region="US",
            number="+1234567890",
            number_type="mobile",
            agency_authorized_representative="Jane Doe",
            agency_representative_email="jane.doe@company.com",
            agreement_last_sent_date=agreement_date,
        )

        # Verify the API call includes the datetime
        call_args = sms_resource.client.post.call_args
        request_data = call_args[1]["json"]
        assert "agreement_last_sent_date" in request_data

    def test_get_available_numbers_success(self, sms_resource):
        """Test getting available numbers successfully."""
        # Setup mock response matching the API spec
        mock_response = Mock()
        mock_response.json.return_value = {
            "numbers": [
                {
                    "features": [
                        {
                            "name": "SMS",
                            "reservable": True,
                            "region_id": "US",
                            "number_type": "mobile",
                            "quickship": True,
                            "region_information": {
                                "region_type": "country",
                                "region_name": "United States",
                            },
                            "phone_number": "+1234567890",
                            "cost_information": {
                                "monthly_cost": "1.00",
                                "setup_cost": "0.00",
                                "currency": "USD",
                            },
                            "best_effort": False,
                            "number_provider_type": "twilio",
                        }
                    ]
                }
            ]
        }
        sms_resource.client.get.return_value = mock_response

        result = sms_resource.get_available_numbers(region="US", limit=10, type="mobile", page=1)

        # Verify the response
        assert len(result.numbers) == 1
        number_info = result.numbers[0]
        assert len(number_info.features) == 1
        feature = number_info.features[0]
        assert feature.phone_number == "+1234567890"
        assert feature.number_type == "mobile"

        # Verify the API call
        call_args = sms_resource.client.get.call_args
        assert call_args[0][0] == "user-api/numbers"
        params = call_args[1]["params"]
        assert params["region"] == "US"
        assert params["limit"] == 10
        assert params["type"] == "mobile"
        assert params["page"] == 1

    def test_get_available_numbers_default_region(self, sms_resource):
        """Test getting available numbers with default region."""
        mock_response = Mock()
        mock_response.json.return_value = {"numbers": []}
        sms_resource.client.get.return_value = mock_response

        sms_resource.get_available_numbers()

        # Verify default region is used
        call_args = sms_resource.client.get.call_args
        params = call_args[1]["params"]
        assert params["region"] == "US"

    def test_get_available_numbers_with_capabilities(self, sms_resource):
        """Test getting available numbers with capabilities filter."""
        mock_response = Mock()
        mock_response.json.return_value = {"numbers": []}
        sms_resource.client.get.return_value = mock_response

        capabilities = ["SMS", "MMS"]
        sms_resource.get_available_numbers(capabilities=capabilities)

        # Verify capabilities are passed
        call_args = sms_resource.client.get.call_args
        params = call_args[1]["params"]
        assert params["capabilities"] == capabilities

    # Legacy method tests for backward compatibility
    def test_legacy_send_method(self, sms_resource, test_phone_number):
        """Test legacy send method for backward compatibility."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "msg_123456789",
            "user_id": "user_123",
            "tenant_id": "tenant_123",
            "sender_id": "sender_123",
            "recipient": test_phone_number,
            "message": "Hello, World!",
            "account_id": "account_123",
            "account_type": "sms",
            "status": "queued",
            "message_timeline": {},
            "message_id": "msg_123456789",
            "bulksmsid": "bulk_123",
            "sent_date": "2024-01-01T12:00:00Z",
            "direction": "sent",
            "recipientcontactid": "contact_123",
            "api_route": "user-api/sms/quick-send",
            "apimode": "quick-send",
            "quicksendidentifier": "quick_123",
            "hirvalidation": True,
        }
        sms_resource.client.post.return_value = mock_response

        # Test legacy method
        result = sms_resource.send(to=test_phone_number, body="Hello, World!", from_="+1987654321")

        # Should return the new response type
        assert result.id == "msg_123456789"
        assert result.recipient == test_phone_number

    def test_legacy_send_without_sender_fails(self, sms_resource, test_phone_number):
        """Test legacy send method fails without sender."""
        with pytest.raises(DevoValidationException, match="Sender .* is required"):
            sms_resource.send(to=test_phone_number, body="Hello, World!")

    def test_legacy_methods_not_implemented(self, sms_resource):
        """Test that unsupported legacy methods don't exist."""
        # These methods were completely removed for cleaner API
        assert not hasattr(sms_resource, "get")
        assert not hasattr(sms_resource, "list")
        assert not hasattr(sms_resource, "cancel")
