from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_required_string, validate_response
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.messages import Message, SendMessageDto, SendMessageSerializer


class MessagesResource(BaseResource):
    """
    Unified messages resource for managing messages across all channels.

    This resource provides a unified interface to send, view and manage messages
    across any channel (SMS, Email, WhatsApp, RCS).
    """

    def send(self, data: "SendMessageDto") -> "SendMessageSerializer":
        """
        Send a message through any channel (omni-channel endpoint).

        This unified endpoint allows sending messages through SMS, Email,
        WhatsApp, or RCS channels using channel-specific payloads.

        Args:
            data: SendMessageDto containing channel, recipient, and payload

        Returns:
            SendMessageSerializer with sent message details

        Example:
            # Send SMS
            from ..models.messages import SendMessageDto

            sms_data = SendMessageDto(
                channel="sms",
                to="+1234567890",
                payload={"text": "Hello World"}
            )
            message = client.messages.send(sms_data)

            # Send Email
            email_data = SendMessageDto(
                channel="email",
                to="user@example.com",
                payload={
                    "subject": "Test Email",
                    "text": "Hello World",
                    "html": "<h1>Hello World</h1>"
                }
            )
            message = client.messages.send(email_data)

            # Send WhatsApp
            whatsapp_data = SendMessageDto(
                channel="whatsapp",
                to="+1234567890",
                payload={
                    "type": "text",
                    "text": {"body": "Hello World"}
                }
            )
            message = client.messages.send(whatsapp_data)

            # Send RCS
            rcs_data = SendMessageDto(
                channel="rcs",
                to="+1234567890",
                payload={
                    "message_type": "text",
                    "text": "Hello World"
                }
            )
            message = client.messages.send(rcs_data)
        """
        from ..models.messages import SendMessageSerializer

        response = self.client.post("messages/send", data=data.model_dump(by_alias=True, exclude_none=True))
        return validate_response(response, SendMessageSerializer)

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
