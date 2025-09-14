import re
from typing import Optional, Type, TypeVar

from pydantic import BaseModel

from .exceptions import DevoInvalidEmailException, DevoInvalidPhoneNumberException, DevoValidationException

T = TypeVar("T", bound=BaseModel)


def validate_phone_number(phone_number: str) -> str:
    """
    Validate and normalize a phone number.

    Args:
        phone_number: The phone number to validate

    Returns:
        str: The normalized phone number

    Raises:
        DevoInvalidPhoneNumberException: If the phone number is invalid
    """
    if not phone_number:
        raise DevoInvalidPhoneNumberException("Phone number is required")

    # Remove all non-digit characters except +
    cleaned = re.sub(r"[^\d+]", "", phone_number)

    # Check if it starts with + and has digits
    if not re.match(r"^\+\d{10,15}$", cleaned):
        raise DevoInvalidPhoneNumberException("Phone number must be in E.164 format (e.g., +1234567890)")

    return cleaned


def validate_email(email: str) -> str:
    """
    Validate an email address.

    Args:
        email: The email address to validate

    Returns:
        str: The validated email address

    Raises:
        DevoInvalidEmailException: If the email is invalid
    """
    if not email:
        raise DevoInvalidEmailException("Email address is required")

    # More comprehensive email validation
    # Basic structure check
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        raise DevoInvalidEmailException("Invalid email address format")

    # Check for consecutive dots
    if ".." in email:
        raise DevoInvalidEmailException("Invalid email address format")

    # Check for dots at the beginning or end of local part
    local_part = email.split("@")[0]
    if local_part.startswith(".") or local_part.endswith("."):
        raise DevoInvalidEmailException("Invalid email address format")

    return email.lower()


def validate_required_string(value: Optional[str], field_name: str) -> str:
    """
    Validate that a string field is present and not empty.

    Args:
        value: The value to validate
        field_name: The name of the field (for error messages)

    Returns:
        str: The validated value

    Raises:
        DevoValidationException: If the value is None or empty
    """
    if not value or not value.strip():
        raise DevoValidationException(f"{field_name} is required and cannot be empty")

    return value.strip()


def format_datetime(dt) -> str:
    """
    Format a datetime object to ISO 8601 string.

    Args:
        dt: datetime object or datetime string

    Returns:
        str: ISO 8601 formatted datetime string
    """
    if isinstance(dt, str):
        return dt

    # Assume it's a datetime object
    return dt.isoformat()


def validate_response(response, model_class: Type[T]) -> T:
    """
    Validate and parse API response into a Pydantic model.

    Args:
        response: HTTP response object with json() method
        model_class: Pydantic model class to parse response into

    Returns:
        Parsed model instance

    Raises:
        DevoValidationException: If response parsing fails
    """
    try:
        data = response.json()
        return model_class(**data)
    except Exception as e:
        raise DevoValidationException(f"Failed to parse response: {str(e)}")


def parse_webhook_signature(signature_header: str) -> dict:
    """
    Parse webhook signature header.

    Args:
        signature_header: The signature header value

    Returns:
        dict: Parsed signature components
    """
    components = {}

    for component in signature_header.split(","):
        if "=" in component:
            key, value = component.strip().split("=", 1)
            components[key] = value

    return components
