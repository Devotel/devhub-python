from datetime import datetime
from unittest.mock import Mock

import pytest

from devo_global_comms_python.exceptions import DevoValidationException
from devo_global_comms_python.resources.email import EmailResource


class TestEmailResource:
    """Test cases for the Email resource with new API implementation."""

    @pytest.fixture
    def email_resource(self, mock_client):
        """Create an Email resource instance."""
        return EmailResource(mock_client)

    def test_send_email_success(self, email_resource):
        """Test sending an email successfully using the new send API."""
        # Setup mock response matching the API spec
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "message_id": "email_123456789",
            "bulk_email_id": "bulk_email_123",
            "subject": "Hello World!",
            "status": "sent",
            "message": "Email sent successfully",
            "timestamp": "2019-08-28T06:25:26.715Z",
        }
        email_resource.client.post.return_value = mock_response

        # Test the send_email method
        result = email_resource.send_email(
            subject="Hello World!",
            body="This is a test email!",
            sender="sender@example.com",
            recipient="recipient@example.com",
        )

        # Verify the request was made correctly
        email_resource.client.post.assert_called_once_with(
            "user-api/email/send",
            json={
                "subject": "Hello World!",
                "body": "This is a test email!",
                "sender": "sender@example.com",
                "recipient": "recipient@example.com",
            },
        )

        # Verify the response is correctly parsed
        assert result.success is True
        assert result.message_id == "email_123456789"
        assert result.bulk_email_id == "bulk_email_123"
        assert result.subject == "Hello World!"
        assert result.status == "sent"
        assert result.message == "Email sent successfully"
        assert result.timestamp == datetime.fromisoformat("2019-08-28T06:25:26.715+00:00")

    def test_send_email_missing_subject(self, email_resource):
        """Test that missing subject raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            email_resource.send_email(
                subject="",
                body="This is a test email!",
                sender="sender@example.com",
                recipient="recipient@example.com",
            )
        assert "subject" in str(exc_info.value)

    def test_send_email_missing_body(self, email_resource):
        """Test that missing body raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            email_resource.send_email(
                subject="Hello World!",
                body="",
                sender="sender@example.com",
                recipient="recipient@example.com",
            )
        assert "body" in str(exc_info.value)

    def test_send_email_invalid_sender_email(self, email_resource):
        """Test that invalid sender email raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            email_resource.send_email(
                subject="Hello World!",
                body="This is a test email!",
                sender="invalid-email",
                recipient="recipient@example.com",
            )
        assert "sender" in str(exc_info.value) or "email" in str(exc_info.value)

    def test_send_email_invalid_recipient_email(self, email_resource):
        """Test that invalid recipient email raises validation error."""
        with pytest.raises(DevoValidationException) as exc_info:
            email_resource.send_email(
                subject="Hello World!",
                body="This is a test email!",
                sender="sender@example.com",
                recipient="invalid-email",
            )
        assert "recipient" in str(exc_info.value) or "email" in str(exc_info.value)

    def test_send_email_with_special_characters(self, email_resource):
        """Test sending email with special characters in subject and body."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "message_id": "email_special_123",
            "bulk_email_id": "bulk_email_special_123",
            "subject": "🎉 Special Test! @#$%^&*()",
            "status": "sent",
            "message": "Email sent successfully",
            "timestamp": "2019-08-28T06:25:26.715Z",
        }
        email_resource.client.post.return_value = mock_response

        special_subject = "🎉 Special Test! @#$%^&*()"
        special_body = "This email contains special characters: àáâäæãåā €£¥₹"

        result = email_resource.send_email(
            subject=special_subject,
            body=special_body,
            sender="test@example.com",
            recipient="recipient@example.com",
        )

        # Verify the request was made with special characters
        email_resource.client.post.assert_called_once_with(
            "user-api/email/send",
            json={
                "subject": special_subject,
                "body": special_body,
                "sender": "test@example.com",
                "recipient": "recipient@example.com",
            },
        )

        assert result.success is True
        assert result.subject == special_subject

    def test_send_email_long_content(self, email_resource):
        """Test sending email with long subject and body."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "message_id": "email_long_123",
            "bulk_email_id": "bulk_email_long_123",
            "subject": "A" * 100,
            "status": "sent",
            "message": "Email sent successfully",
            "timestamp": "2019-08-28T06:25:26.715Z",
        }
        email_resource.client.post.return_value = mock_response

        long_subject = "A" * 100
        long_body = "B" * 1000

        result = email_resource.send_email(
            subject=long_subject,
            body=long_body,
            sender="sender@example.com",
            recipient="recipient@example.com",
        )

        email_resource.client.post.assert_called_once_with(
            "user-api/email/send",
            json={
                "subject": long_subject,
                "body": long_body,
                "sender": "sender@example.com",
                "recipient": "recipient@example.com",
            },
        )

        assert result.success is True

    def test_send_email_api_error_handling(self, email_resource):
        """Test that API errors are properly handled."""
        # Mock an API error response
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": False,
            "message_id": "",
            "bulk_email_id": "",
            "subject": "",
            "status": "failed",
            "message": "Invalid recipient email address",
            "timestamp": "2019-08-28T06:25:26.715Z",
        }
        email_resource.client.post.return_value = mock_response

        result = email_resource.send_email(
            subject="Test Subject",
            body="Test Body",
            sender="sender@example.com",
            recipient="recipient@example.com",
        )

        assert result.success is False
        assert result.status == "failed"
        assert result.message == "Invalid recipient email address"

    def test_send_email_different_email_formats(self, email_resource):
        """Test sending emails with different valid email formats."""
        test_cases = [
            ("user@domain.com", "user@domain.com"),
            ("user.name@domain.co.uk", "user.name@domain.co.uk"),
            ("user+tag@domain.org", "user+tag@domain.org"),
            ("user123@sub.domain.com", "user123@sub.domain.com"),
        ]

        for sender, recipient in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = {
                "success": True,
                "message_id": f"email_{sender.replace('@', '_').replace('.', '_')}",
                "bulk_email_id": "bulk_email_format_test",
                "subject": "Format Test",
                "status": "sent",
                "message": "Email sent successfully",
                "timestamp": "2019-08-28T06:25:26.715Z",
            }
            email_resource.client.post.return_value = mock_response

            result = email_resource.send_email(
                subject="Format Test",
                body="Testing different email formats",
                sender=sender,
                recipient=recipient,
            )

            assert result.success is True
            assert result.status == "sent"

    def test_send_email_unicode_content(self, email_resource):
        """Test sending email with Unicode content."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "message_id": "email_unicode_123",
            "bulk_email_id": "bulk_email_unicode_123",
            "subject": "Unicode Test: 你好世界",
            "status": "sent",
            "message": "Email sent successfully",
            "timestamp": "2019-08-28T06:25:26.715Z",
        }
        email_resource.client.post.return_value = mock_response

        unicode_subject = "Unicode Test: 你好世界"
        unicode_body = "Unicode content: Здравствуй мир! مرحبا بالعالم"

        result = email_resource.send_email(
            subject=unicode_subject,
            body=unicode_body,
            sender="sender@example.com",
            recipient="recipient@example.com",
        )

        email_resource.client.post.assert_called_once_with(
            "user-api/email/send",
            json={
                "subject": unicode_subject,
                "body": unicode_body,
                "sender": "sender@example.com",
                "recipient": "recipient@example.com",
            },
        )

        assert result.success is True

    def test_send_email_whitespace_handling(self, email_resource):
        """Test that whitespace in subject and body is handled correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "message_id": "email_whitespace_123",
            "bulk_email_id": "bulk_email_whitespace_123",
            "subject": "  Test Subject  ",
            "status": "sent",
            "message": "Email sent successfully",
            "timestamp": "2019-08-28T06:25:26.715Z",
        }
        email_resource.client.post.return_value = mock_response

        # Test that emails with whitespace in subject/body are accepted
        # but email addresses must be properly formatted
        result = email_resource.send_email(
            subject="  Test Subject  ",
            body="  Test Body  ",
            sender="sender@example.com",
            recipient="recipient@example.com",
        )

        # Should call with the exact values provided
        assert email_resource.client.post.called
        assert result.success is True
