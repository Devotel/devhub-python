from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_email, validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.contacts import Contact


class ContactsResource(BaseResource):
    """Contacts resource for managing contact information."""

    def create(
        self,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Contact":
        """Create a new contact."""
        if not phone_number and not email:
            raise ValueError("Either phone_number or email must be provided")

        data = {}

        if phone_number:
            data["phone_number"] = validate_phone_number(phone_number)
        if email:
            data["email"] = validate_email(email)
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if company:
            data["company"] = company
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("contacts", json=data)

        from ..models.contacts import Contact

        return Contact.parse_obj(response.json())

    def get(self, contact_id: str) -> "Contact":
        """Retrieve a contact by ID."""
        contact_id = validate_required_string(contact_id, "contact_id")
        response = self.client.get(f"contacts/{contact_id}")

        from ..models.contacts import Contact

        return Contact.parse_obj(response.json())

    def update(
        self,
        contact_id: str,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Contact":
        """Update an existing contact."""
        contact_id = validate_required_string(contact_id, "contact_id")

        data = {}
        if phone_number:
            data["phone_number"] = validate_phone_number(phone_number)
        if email:
            data["email"] = validate_email(email)
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if company:
            data["company"] = company
        if metadata:
            data["metadata"] = metadata

        response = self.client.put(f"contacts/{contact_id}", json=data)

        from ..models.contacts import Contact

        return Contact.parse_obj(response.json())

    def delete(self, contact_id: str) -> bool:
        """Delete a contact."""
        contact_id = validate_required_string(contact_id, "contact_id")
        response = self.client.delete(f"contacts/{contact_id}")
        return response.status_code == 204

    def list(
        self,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List["Contact"]:
        """List contacts with optional filtering."""
        params = {"limit": limit, "offset": offset}

        if phone_number:
            params["phone_number"] = validate_phone_number(phone_number)
        if email:
            params["email"] = validate_email(email)
        if company:
            params["company"] = company

        response = self.client.get("contacts", params=params)
        data = response.json()

        from ..models.contacts import Contact

        return [Contact.parse_obj(item) for item in data.get("contacts", [])]
