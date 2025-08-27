"""
SMS resource for the Devo Global Communications API.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.sms import SMSMessage


class SMSResource(BaseResource):
    """
    SMS resource for sending and managing SMS messages.

    Example:
        >>> message = client.sms.send(
        ...     to="+1234567890",
        ...     body="Hello, World!"
        ... )
        >>> print(message.sid)
    """

    def send(
        self,
        to: str,
        body: str,
        from_: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "SMSMessage":
        """
        Send an SMS message.

        Args:
            to: The recipient's phone number in E.164 format
            body: The message body text
            from_: The sender's phone number (optional, uses account default)
            media_urls: List of media URLs for MMS (optional)
            callback_url: Webhook URL for delivery status (optional)
            metadata: Custom metadata dictionary (optional)

        Returns:
            SMSMessage: The sent message details

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error
        """
        # Validate inputs
        to = validate_phone_number(to)
        body = validate_required_string(body, "body")

        if from_:
            from_ = validate_phone_number(from_)

        # Prepare request data
        data = {
            "to": to,
            "body": body,
        }

        if from_:
            data["from"] = from_
        if media_urls:
            data["media_urls"] = media_urls
        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        # Send request
        response = self.client.post("sms/messages", json=data)

        # Import here to avoid circular imports
        from ..models.sms import SMSMessage

        return SMSMessage.parse_obj(response.json())

    def get(self, message_sid: str) -> "SMSMessage":
        """
        Retrieve an SMS message by SID.

        Args:
            message_sid: The message SID

        Returns:
            SMSMessage: The message details
        """
        message_sid = validate_required_string(message_sid, "message_sid")

        response = self.client.get(f"sms/messages/{message_sid}")

        from ..models.sms import SMSMessage

        return SMSMessage.parse_obj(response.json())

    def list(
        self,
        to: Optional[str] = None,
        from_: Optional[str] = None,
        date_sent_after: Optional[str] = None,
        date_sent_before: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List["SMSMessage"]:
        """
        List SMS messages with optional filtering.

        Args:
            to: Filter by recipient phone number
            from_: Filter by sender phone number
            date_sent_after: Filter messages sent after this date
            date_sent_before: Filter messages sent before this date
            status: Filter by message status
            limit: Maximum number of messages to return (default: 50)
            offset: Number of messages to skip (default: 0)

        Returns:
            List[SMSMessage]: List of messages
        """
        params = {
            "limit": limit,
            "offset": offset,
        }

        if to:
            params["to"] = validate_phone_number(to)
        if from_:
            params["from"] = validate_phone_number(from_)
        if date_sent_after:
            params["date_sent_after"] = date_sent_after
        if date_sent_before:
            params["date_sent_before"] = date_sent_before
        if status:
            params["status"] = status

        response = self.client.get("sms/messages", params=params)
        data = response.json()

        from ..models.sms import SMSMessage

        return [SMSMessage.parse_obj(item) for item in data.get("messages", [])]

    def cancel(self, message_sid: str) -> "SMSMessage":
        """
        Cancel a scheduled SMS message.

        Args:
            message_sid: The message SID to cancel

        Returns:
            SMSMessage: The updated message details
        """
        message_sid = validate_required_string(message_sid, "message_sid")

        response = self.client.delete(f"sms/messages/{message_sid}")

        from ..models.sms import SMSMessage

        return SMSMessage.parse_obj(response.json())
