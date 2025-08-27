from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..utils import validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.messages import Message


class MessagesResource(BaseResource):
    """
    Unified messages resource for managing messages across all channels.

    This resource provides a unified interface to view and manage messages
    sent through any channel (SMS, Email, WhatsApp, RCS).
    """

    def get(self, message_id: str) -> "Message":
        """
        Retrieve a message by ID from any channel.

        Args:
            message_id: The message ID

        Returns:
            Message: The message details
        """
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.get(f"messages/{message_id}")

        from ..models.messages import Message

        return Message.parse_obj(response.json())

    def list(
        self,
        channel: Optional[str] = None,
        to: Optional[str] = None,
        from_: Optional[str] = None,
        status: Optional[str] = None,
        date_sent_after: Optional[str] = None,
        date_sent_before: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List["Message"]:
        """
        List messages across all channels with optional filtering.

        Args:
            channel: Filter by channel (sms, email, whatsapp, rcs)
            to: Filter by recipient
            from_: Filter by sender
            status: Filter by message status
            date_sent_after: Filter messages sent after this date
            date_sent_before: Filter messages sent before this date
            limit: Maximum number of messages to return (default: 50)
            offset: Number of messages to skip (default: 0)

        Returns:
            List[Message]: List of messages
        """
        params = {"limit": limit, "offset": offset}

        if channel:
            params["channel"] = channel
        if to:
            params["to"] = to
        if from_:
            params["from"] = from_
        if status:
            params["status"] = status
        if date_sent_after:
            params["date_sent_after"] = date_sent_after
        if date_sent_before:
            params["date_sent_before"] = date_sent_before

        response = self.client.get("messages", params=params)
        data = response.json()

        from ..models.messages import Message

        return [Message.parse_obj(item) for item in data.get("messages", [])]

    def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """
        Get detailed delivery status for a message.

        Args:
            message_id: The message ID

        Returns:
            Dict[str, Any]: Delivery status details
        """
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.get(f"messages/{message_id}/delivery-status")
        return response.json()

    def resend(self, message_id: str) -> "Message":
        """
        Resend a failed message.

        Args:
            message_id: The message ID to resend

        Returns:
            Message: The new message details
        """
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.post(f"messages/{message_id}/resend")

        from ..models.messages import Message

        return Message.parse_obj(response.json())
