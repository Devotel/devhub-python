from typing import TYPE_CHECKING

from ..utils import validate_email, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.email import EmailSendResponse


class EmailResource(BaseResource):
    """
    Email resource for sending and managing email messages.

    Example:
        >>> response = client.email.send_email(
        ...     subject="Hello, World!",
        ...     body="This is a test email.",
        ...     sender="sender@example.com",
        ...     recipient="recipient@example.com"
        ... )
        >>> print(response.message_id)
    """

    def send_email(
        self,
        subject: str,
        body: str,
        sender: str,
        recipient: str,
    ) -> "EmailSendResponse":
        """
        Send an email using the exact API specification.

        Args:
            subject: Email subject
            body: Email body content
            sender: Sender email address
            recipient: Recipient email address

        Returns:
            EmailSendResponse: The email send response
        """
        # Validate inputs
        subject = validate_required_string(subject, "subject")
        body = validate_required_string(body, "body")
        sender = validate_email(sender)
        recipient = validate_email(recipient)

        # Prepare request data matching the exact API specification
        data = {
            "subject": subject,
            "body": body,
            "sender": sender,
            "recipient": recipient,
        }

        # Send request to the exact endpoint
        response = self.client.post("user-api/email/send", json=data)

        from ..models.email import EmailSendResponse

        return EmailSendResponse.model_validate(response.json())
