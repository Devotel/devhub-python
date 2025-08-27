from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.rcs import RCSMessage


class RCSResource(BaseResource):
    """RCS (Rich Communication Services) resource for sending and managing RCS messages."""

    def send_text(
        self,
        to: str,
        text: str,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "RCSMessage":
        """Send an RCS text message."""
        to = validate_phone_number(to)
        text = validate_required_string(text, "text")

        data = {"to": to, "type": "text", "text": text}
        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("rcs/messages", json=data)

        from ..models.rcs import RCSMessage

        return RCSMessage.parse_obj(response.json())

    def send_rich_card(
        self,
        to: str,
        title: str,
        description: str,
        media_url: Optional[str] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "RCSMessage":
        """Send an RCS rich card message."""
        to = validate_phone_number(to)
        title = validate_required_string(title, "title")
        description = validate_required_string(description, "description")

        data = {
            "to": to,
            "type": "rich_card",
            "rich_card": {
                "title": title,
                "description": description,
            },
        }

        if media_url:
            data["rich_card"]["media_url"] = media_url
        if actions:
            data["rich_card"]["actions"] = actions
        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("rcs/messages", json=data)

        from ..models.rcs import RCSMessage

        return RCSMessage.parse_obj(response.json())

    def get(self, message_id: str) -> "RCSMessage":
        """Retrieve an RCS message by ID."""
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.get(f"rcs/messages/{message_id}")

        from ..models.rcs import RCSMessage

        return RCSMessage.parse_obj(response.json())
