from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.whatsapp import WhatsAppMessage


class WhatsAppResource(BaseResource):
    """WhatsApp resource for sending and managing WhatsApp messages."""

    def send_text(
        self,
        to: str,
        text: str,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "WhatsAppMessage":
        """Send a WhatsApp text message."""
        to = validate_phone_number(to)
        text = validate_required_string(text, "text")

        data = {"to": to, "type": "text", "text": {"body": text}}
        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("whatsapp/messages", json=data)

        from ..models.whatsapp import WhatsAppMessage

        return WhatsAppMessage.parse_obj(response.json())

    def send_template(
        self,
        to: str,
        template_name: str,
        language: str = "en",
        parameters: Optional[List[str]] = None,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "WhatsAppMessage":
        """Send a WhatsApp template message."""
        to = validate_phone_number(to)
        template_name = validate_required_string(template_name, "template_name")

        data = {
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language},
            },
        }

        if parameters:
            data["template"]["components"] = [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": p} for p in parameters],
                }
            ]

        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("whatsapp/messages", json=data)

        from ..models.whatsapp import WhatsAppMessage

        return WhatsAppMessage.parse_obj(response.json())

    def get(self, message_id: str) -> "WhatsAppMessage":
        """Retrieve a WhatsApp message by ID."""
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.get(f"whatsapp/messages/{message_id}")

        from ..models.whatsapp import WhatsAppMessage

        return WhatsAppMessage.parse_obj(response.json())
