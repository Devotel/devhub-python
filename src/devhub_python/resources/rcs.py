from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.rcs import RcsAccountSerializer, RCSMessage, RcsSendMessageSerializer, SuccessSerializer


class RCSResource(BaseResource):
    """RCS (Rich Communication Services) resource for managing accounts, templates, brands, and messaging."""

    # Account Management Endpoints
    def create_account(self, account_data: Dict[str, Any]) -> "RcsAccountSerializer":
        """Submit RCS Account."""
        response = self.client.post("user-api/rcs/accounts", json=account_data)

        from ..models.rcs import RcsAccountSerializer

        return RcsAccountSerializer.model_validate(response.json())

    def get_accounts(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        id: Optional[str] = None,
        is_approved: Optional[str] = None,
    ) -> List["RcsAccountSerializer"]:
        """Get all RCS Accounts."""
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if id is not None:
            params["id"] = id
        if is_approved is not None:
            params["isApproved"] = is_approved

        response = self.client.get("user-api/rcs/accounts", params=params)
        data = response.json()

        # If the response contains a nested structure (like {"rcsAccounts": [...]}),
        # extract the accounts list for backward compatibility
        if isinstance(data, dict) and "rcsAccounts" in data:
            accounts_data = data["rcsAccounts"]
        elif isinstance(data, list):
            accounts_data = data
        else:
            # Fallback - use the data as-is
            accounts_data = data

        # Ensure we have a list to work with
        if not isinstance(accounts_data, list):
            accounts_data = []

        # Parse each account into RcsAccountSerializer objects
        from ..models.rcs import RcsAccountSerializer

        return [RcsAccountSerializer.model_validate(account) for account in accounts_data]

    def verify_account(self, verification_data: Dict[str, Any]) -> "SuccessSerializer":
        """Verify RCS Account."""
        response = self.client.post("/api/v1/user-api/rcs/accounts/verify", json=verification_data)

        from ..models.rcs import SuccessSerializer

        return SuccessSerializer.model_validate(response.json())

    def update_account(self, account_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update RCS Account."""
        account_id = validate_required_string(account_id, "account_id")
        response = self.client.put(f"/api/v1/user-api/rcs/accounts/{account_id}", json=account_data)
        return response.json()

    def get_account_details(self, account_id: str) -> Dict[str, Any]:
        """Get Account Details."""
        account_id = validate_required_string(account_id, "account_id")
        response = self.client.get(f"/api/v1/user-api/rcs/accounts/{account_id}")
        return response.json()

    # Messaging Endpoints
    def send_message(self, message_data: Dict[str, Any]) -> "RcsSendMessageSerializer":
        """Send RCS message."""
        response = self.client.post("/api/v1/user-api/rcs/send", json=message_data)

        from ..models.rcs import RcsSendMessageSerializer

        return RcsSendMessageSerializer.model_validate(response.json())

    def list_messages(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        id: Optional[str] = None,
        type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List["RcsSendMessageSerializer"]:
        """List Messages."""
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if id is not None:
            params["id"] = id
        if type is not None:
            params["type"] = type
        if search is not None:
            params["search"] = search

        response = self.client.get("/api/v1/user-api/rcs/messages", params=params)

        from ..models.rcs import RcsSendMessageSerializer

        return [RcsSendMessageSerializer.model_validate(message) for message in response.json()]

    # Template Management Endpoints
    def create_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create RCS templates."""
        response = self.client.post("/api/v1/user-api/rcs/templates", json=template_data)
        return response.json()

    def get_templates(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get all RCS templates."""
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if id is not None:
            params["id"] = id

        response = self.client.get("user-api/rcs/templates", params=params)
        return response.json()

    def delete_template(self, delete_data: Dict[str, Any], approve: Optional[str] = None) -> Dict[str, Any]:
        """Delete RCS templates."""
        params = {}
        if approve is not None:
            params["approve"] = approve

        response = self.client.delete("/api/v1/user-api/rcs/templates", json=delete_data, params=params)
        return response.json()

    def update_template(self, template_id: str, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update RCS templates."""
        template_id = validate_required_string(template_id, "template_id")
        response = self.client.put(f"/api/v1/user-api/rcs/templates/{template_id}", json=template_data)
        return response.json()

    # Brand Management Endpoints
    def get_brands(
        self,
        id: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get all RCS Brands."""
        params = {}
        if id is not None:
            params["id"] = id
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if search is not None:
            params["search"] = search

        response = self.client.get("user-api/rcs/brands", params=params)
        return response.json()

    def create_brand(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create RCS Brands."""
        response = self.client.post("/api/v1/user-api/rcs/brands", json=brand_data)
        return response.json()

    def update_brand(self, brand_id: str, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update RCS Brands."""
        brand_id = validate_required_string(brand_id, "brand_id")
        response = self.client.put(f"/api/v1/user-api/rcs/brands/{brand_id}", json=brand_data)
        return response.json()

    # Tester Management Endpoints
    def add_tester(self, tester_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add RCS Tester."""
        response = self.client.post("/api/v1/user-api/rcs/testers", json=tester_data)
        return response.json()

    def get_testers(
        self,
        account_id: str,
        id: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get RCS Testers."""
        account_id = validate_required_string(account_id, "account_id")
        params = {"account_id": account_id}
        if id is not None:
            params["id"] = id
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if search is not None:
            params["search"] = search

        response = self.client.get("/api/v1/user-api/rcs/testers", params=params)
        return response.json()

    # Legacy methods for backward compatibility
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

        return RCSMessage.model_validate(response.json())

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

        return RCSMessage.model_validate(response.json())

    def get(self, message_id: str) -> "RCSMessage":
        """Retrieve an RCS message by ID."""
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.get(f"rcs/messages/{message_id}")

        from ..models.rcs import RCSMessage

        return RCSMessage.model_validate(response.json())
