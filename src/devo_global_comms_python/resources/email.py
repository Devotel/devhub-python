from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_email, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.email import EmailMessage


class EmailResource(BaseResource):
    """
    Email resource for sending and managing email messages.

    Example:
        >>> message = client.email.send(
        ...     to="recipient@example.com",
        ...     subject="Hello, World!",
        ...     body="This is a test email."
        ... )
        >>> print(message.id)
    """

    def send(
        self,
        to: str,
        subject: str,
        body: str,
        from_: Optional[str] = None,
        html_body: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        reply_to: Optional[str] = None,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "EmailMessage":
        """
        Send an email message.

        Args:
            to: The recipient's email address
            subject: The email subject
            body: The plain text email body
            from_: The sender's email address (optional, uses account default)
            html_body: The HTML email body (optional)
            cc: List of CC email addresses (optional)
            bcc: List of BCC email addresses (optional)
            attachments: List of attachment objects (optional)
            reply_to: Reply-to email address (optional)
            callback_url: Webhook URL for delivery status (optional)
            metadata: Custom metadata dictionary (optional)

        Returns:
            EmailMessage: The sent message details
        """
        # Validate inputs
        to = validate_email(to)
        subject = validate_required_string(subject, "subject")
        body = validate_required_string(body, "body")

        if from_:
            from_ = validate_email(from_)
        if reply_to:
            reply_to = validate_email(reply_to)
        if cc:
            cc = [validate_email(email) for email in cc]
        if bcc:
            bcc = [validate_email(email) for email in bcc]

        # Prepare request data
        data = {
            "to": to,
            "subject": subject,
            "body": body,
        }

        if from_:
            data["from"] = from_
        if html_body:
            data["html_body"] = html_body
        if cc:
            data["cc"] = cc
        if bcc:
            data["bcc"] = bcc
        if attachments:
            data["attachments"] = attachments
        if reply_to:
            data["reply_to"] = reply_to
        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        # Send request
        response = self.client.post("email/messages", json=data)

        from ..models.email import EmailMessage

        return EmailMessage.parse_obj(response.json())

    def get(self, message_id: str) -> "EmailMessage":
        """
        Retrieve an email message by ID.

        Args:
            message_id: The message ID

        Returns:
            EmailMessage: The message details
        """
        message_id = validate_required_string(message_id, "message_id")

        response = self.client.get(f"email/messages/{message_id}")

        from ..models.email import EmailMessage

        return EmailMessage.parse_obj(response.json())

    def list(
        self,
        to: Optional[str] = None,
        from_: Optional[str] = None,
        subject: Optional[str] = None,
        date_sent_after: Optional[str] = None,
        date_sent_before: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List["EmailMessage"]:
        """
        List email messages with optional filtering.

        Args:
            to: Filter by recipient email address
            from_: Filter by sender email address
            subject: Filter by subject (partial match)
            date_sent_after: Filter messages sent after this date
            date_sent_before: Filter messages sent before this date
            status: Filter by message status
            limit: Maximum number of messages to return (default: 50)
            offset: Number of messages to skip (default: 0)

        Returns:
            List[EmailMessage]: List of messages
        """
        params = {
            "limit": limit,
            "offset": offset,
        }

        if to:
            params["to"] = validate_email(to)
        if from_:
            params["from"] = validate_email(from_)
        if subject:
            params["subject"] = subject
        if date_sent_after:
            params["date_sent_after"] = date_sent_after
        if date_sent_before:
            params["date_sent_before"] = date_sent_before
        if status:
            params["status"] = status

        response = self.client.get("email/messages", params=params)
        data = response.json()

        from ..models.email import EmailMessage

        return [EmailMessage.parse_obj(item) for item in data.get("messages", [])]
