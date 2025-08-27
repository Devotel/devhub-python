from datetime import datetime

import pytest

from devo_global_comms_python.exceptions import (
    DevoInvalidEmailException,
    DevoInvalidPhoneNumberException,
    DevoValidationException,
)
from devo_global_comms_python.utils import (
    format_datetime,
    parse_webhook_signature,
    validate_email,
    validate_phone_number,
    validate_required_string,
)


class TestValidationUtils:
    """Test cases for validation utility functions."""

    def test_validate_phone_number_valid(self):
        """Test phone number validation with valid numbers."""
        valid_numbers = [
            "+1234567890",
            "+447123456789",
            "+86123456789012",
        ]

        for number in valid_numbers:
            result = validate_phone_number(number)
            assert result == number

    def test_validate_phone_number_with_formatting(self):
        """Test phone number validation removes formatting."""
        formatted_numbers = [
            "+1 (234) 567-8900",
            "+1-234-567-8900",
            "+1.234.567.8900",
            "+1 234 567 8900",
        ]

        expected = "+12345678900"

        for number in formatted_numbers:
            result = validate_phone_number(number)
            assert result == expected

    def test_validate_phone_number_invalid(self):
        """Test phone number validation with invalid numbers."""
        invalid_numbers = [
            "",
            "1234567890",  # Missing +
            "+123",  # Too short
            "+123456789012345678",  # Too long
            "invalid",
            "+abc123456789",
        ]

        for number in invalid_numbers:
            with pytest.raises(DevoInvalidPhoneNumberException):
                validate_phone_number(number)

    def test_validate_email_valid(self):
        """Test email validation with valid addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@example.com",
        ]

        for email in valid_emails:
            result = validate_email(email)
            assert result == email.lower()

    def test_validate_email_invalid(self):
        """Test email validation with invalid addresses."""
        invalid_emails = [
            "",
            "invalid",
            "@example.com",
            "test@",
            "test@.com",
            "test..test@example.com",
        ]

        for email in invalid_emails:
            with pytest.raises(DevoInvalidEmailException):
                validate_email(email)

    def test_validate_required_string_valid(self):
        """Test required string validation with valid strings."""
        valid_strings = [
            "hello",
            "  hello  ",  # Should be trimmed
            "hello world",
        ]

        for string in valid_strings:
            result = validate_required_string(string, "test_field")
            assert result == string.strip()

    def test_validate_required_string_invalid(self):
        """Test required string validation with invalid strings."""
        invalid_strings = [
            None,
            "",
            "   ",  # Only whitespace
        ]

        for string in invalid_strings:
            with pytest.raises(DevoValidationException):
                validate_required_string(string, "test_field")


class TestUtilityFunctions:
    """Test cases for general utility functions."""

    def test_format_datetime_with_datetime_object(self):
        """Test datetime formatting with datetime object."""
        dt = datetime(2024, 1, 15, 12, 30, 45)
        result = format_datetime(dt)
        assert result == "2024-01-15T12:30:45"

    def test_format_datetime_with_string(self):
        """Test datetime formatting with string."""
        dt_string = "2024-01-15T12:30:45"
        result = format_datetime(dt_string)
        assert result == dt_string

    def test_parse_webhook_signature(self):
        """Test webhook signature parsing."""
        signature = "t=1234567890,v1=hash123,v2=hash456"
        result = parse_webhook_signature(signature)

        expected = {"t": "1234567890", "v1": "hash123", "v2": "hash456"}

        assert result == expected

    def test_parse_webhook_signature_empty(self):
        """Test webhook signature parsing with empty string."""
        result = parse_webhook_signature("")
        assert result == {}

    def test_parse_webhook_signature_malformed(self):
        """Test webhook signature parsing with malformed input."""
        signature = "invalid,format,no=equals"
        result = parse_webhook_signature(signature)

        # Should only include valid key=value pairs
        assert "no" in result
        assert len(result) == 1
