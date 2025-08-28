"""
SMS resource for the Devo Global Communications API.

Implements SMS API endpoints for sending messages and managing phone numbers.
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from ..exceptions import DevoValidationException
from ..utils import validate_email, validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.sms import AvailableNumbersResponse, NumberPurchaseResponse, SendersListResponse, SMSQuickSendResponse

logger = logging.getLogger(__name__)


class SMSResource(BaseResource):
    """
    SMS resource for sending messages and managing phone numbers.

    This resource provides access to SMS functionality including:
    - Sending SMS messages via quick-send
    - Managing senders and phone numbers
    - Purchasing new phone numbers
    - Listing available numbers

    Examples:
        Send SMS:
        >>> response = client.sms.send_sms(
        ...     recipient="+1234567890",
        ...     message="Hello World!",
        ...     sender="+0987654321"
        ... )

        Get senders:
        >>> senders = client.sms.get_senders()
        >>> for sender in senders.senders:
        ...     print(f"Sender: {sender.phone_number}")

        Buy number:
        >>> number = client.sms.buy_number(
        ...     region="US",
        ...     number="+1234567890",
        ...     number_type="mobile",
        ...     agency_authorized_representative="Jane Doe",
        ...     agency_representative_email="jane.doe@company.com"
        ... )

        List available numbers:
        >>> numbers = client.sms.get_available_numbers(
        ...     region="US",
        ...     limit=10,
        ...     number_type="mobile"
        ... )
    """

    def send_sms(
        self,
        recipient: str,
        message: str,
        sender: str,
        hirvalidation: bool = True,
    ) -> "SMSQuickSendResponse":
        """
        Send an SMS message using the quick-send API.

        Args:
            recipient: The recipient's phone number in E.164 format
            message: The SMS message content
            sender: The sender phone number or sender ID
            hirvalidation: Enable HIR validation (default: True)

        Returns:
            SMSQuickSendResponse: The sent message details including ID and status

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> response = client.sms.send_sms(
            ...     recipient="+1234567890",
            ...     message="Hello World!",
            ...     sender="+0987654321"
            ... )
            >>> print(f"Message ID: {response.id}")
            >>> print(f"Status: {response.status}")
        """
        # Validate inputs
        recipient = validate_phone_number(recipient)
        message = validate_required_string(message, "message")
        sender = validate_required_string(sender, "sender")

        logger.info(f"Sending SMS to {recipient} from {sender}")

        # Prepare request data according to API spec
        from ..models.sms import SMSQuickSendRequest

        request_data = SMSQuickSendRequest(
            sender=sender,
            recipient=recipient,
            message=message,
            hirvalidation=hirvalidation,
        )

        # Send request to the exact API endpoint
        response = self.client.post("user-api/sms/quick-send", json=request_data.dict())

        # Parse response according to API spec
        from ..models.sms import SMSQuickSendResponse

        result = SMSQuickSendResponse.parse_obj(response.json())
        logger.info(f"SMS sent successfully with ID: {result.id}")

        return result

    def get_senders(self) -> "SendersListResponse":
        """
        Retrieve the list of available senders for the account.

        Returns:
            SendersListResponse: List of available senders with their details

        Raises:
            DevoAPIException: If the API returns an error

        Example:
            >>> senders = client.sms.get_senders()
            >>> for sender in senders.senders:
            ...     print(f"Sender: {sender.phone_number} (Type: {sender.type})")
            ...     print(f"Is Test: {sender.istest}")
        """
        logger.info("Fetching available senders")

        # Send request to the exact API endpoint
        response = self.client.get("user-api/me/senders")

        # Parse response according to API spec
        from ..models.sms import SendersListResponse

        result = SendersListResponse.parse_obj(response.json())
        logger.info(f"Retrieved {len(result.senders)} senders")

        return result

    def buy_number(
        self,
        region: str,
        number: str,
        number_type: str,
        agency_authorized_representative: str,
        agency_representative_email: str,
        is_longcode: bool = True,
        agreement_last_sent_date: Optional[datetime] = None,
        is_automated_enabled: bool = True,
    ) -> "NumberPurchaseResponse":
        """
        Purchase a phone number.

        Args:
            region: Region/country code for the number
            number: Phone number to purchase
            number_type: Type of number (mobile, landline, etc.)
            agency_authorized_representative: Name of authorized representative
            agency_representative_email: Email of authorized representative
            is_longcode: Whether this is a long code number (default: True)
            agreement_last_sent_date: Last date agreement was sent (optional)
            is_automated_enabled: Whether automated messages are enabled (default: True)

        Returns:
            NumberPurchaseResponse: Details of the purchased number including features

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> number = client.sms.buy_number(
            ...     region="US",
            ...     number="+1234567890",
            ...     number_type="mobile",
            ...     agency_authorized_representative="Jane Doe",
            ...     agency_representative_email="jane.doe@company.com"
            ... )
            >>> print(f"Purchased number with {len(number.features)} features")
        """
        # Validate inputs
        region = validate_required_string(region, "region")
        number = validate_phone_number(number)
        number_type = validate_required_string(number_type, "number_type")
        agency_authorized_representative = validate_required_string(
            agency_authorized_representative, "agency_authorized_representative"
        )
        agency_representative_email = validate_email(agency_representative_email)

        logger.info(f"Purchasing number {number} in region {region}")

        # Prepare request data according to API spec
        from ..models.sms import NumberPurchaseRequest

        request_data = NumberPurchaseRequest(
            region=region,
            number=number,
            number_type=number_type,
            is_longcode=is_longcode,
            agreement_last_sent_date=agreement_last_sent_date,
            agency_authorized_representative=agency_authorized_representative,
            agency_representative_email=agency_representative_email,
            is_automated_enabled=is_automated_enabled,
        )

        # Send request to the exact API endpoint
        response = self.client.post("user-api/numbers/buy", json=request_data.dict(exclude_none=True))

        # Parse response according to API spec
        from ..models.sms import NumberPurchaseResponse

        result = NumberPurchaseResponse.parse_obj(response.json())
        logger.info(f"Number purchased successfully with {len(result.features)} features")

        return result

    def get_available_numbers(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        capabilities: Optional[List[str]] = None,
        type: Optional[str] = None,
        prefix: Optional[str] = None,
        region: str = "US",
    ) -> "AvailableNumbersResponse":
        """
        Get available phone numbers for purchase.

        Args:
            page: The page number (optional)
            limit: The page limit (optional)
            capabilities: Filter by capabilities (optional)
            type: Filter by type (optional)
            prefix: Filter by prefix (optional)
            region: Filter by region (Country ISO Code), default: "US"

        Returns:
            AvailableNumbersResponse: List of available numbers with their features

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> numbers = client.sms.get_available_numbers(
            ...     region="US",
            ...     limit=10,
            ...     type="mobile"
            ... )
            >>> for number_info in numbers.numbers:
            ...     for feature in number_info.features:
            ...         print(f"Number: {feature.phone_number}")
            ...         print(f"Cost: {feature.cost_information.monthly_cost}")
        """
        logger.info(f"Fetching available numbers for region {region}")

        # Prepare query parameters
        params = {"region": region}

        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if capabilities is not None:
            params["capabilities"] = capabilities
        if type is not None:
            params["type"] = type
        if prefix is not None:
            params["prefix"] = prefix

        # Send request to the exact API endpoint
        response = self.client.get("user-api/numbers", params=params)

        # Parse response according to API spec
        from ..models.sms import AvailableNumbersResponse

        result = AvailableNumbersResponse.parse_obj(response.json())
        logger.info(f"Retrieved {len(result.numbers)} available numbers")

        return result

    # Legacy methods for backward compatibility
    def send(self, to: str, body: str, from_: Optional[str] = None, **kwargs) -> "SMSQuickSendResponse":
        """
        Legacy method for sending SMS (backward compatibility).

        Args:
            to: The recipient's phone number in E.164 format
            body: The message body text
            from_: The sender's phone number (optional)
            **kwargs: Additional parameters (ignored for compatibility)

        Returns:
            SMSQuickSendResponse: The sent message details

        Note:
            This method is deprecated. Use send_sms() instead.
        """
        if not from_:
            raise DevoValidationException("Sender (from_) is required for SMS sending")

        return self.send_sms(
            recipient=to,
            message=body,
            sender=from_,
            hirvalidation=kwargs.get("hirvalidation", True),
        )

    def get(self, message_id: str) -> dict:
        """
        Legacy method for getting message details (backward compatibility).

        Args:
            message_id: The message ID

        Returns:
            dict: Message details

        Note:
            This method provides basic compatibility but may not return
            the full SMSMessage model structure.
        """
        # This would need to be implemented based on a separate API endpoint
        # if available, or could be removed if not supported by the API
        raise NotImplementedError(
            "Message retrieval by ID is not supported by the current API. "
            "Use send_sms() to get message details upon sending."
        )

    def list(self, **kwargs) -> List[dict]:
        """
        Legacy method for listing messages (backward compatibility).

        Returns:
            List[dict]: List of messages

        Note:
            This method provides basic compatibility but may not return
            the full message structure. Consider using get_senders() or
            get_available_numbers() for current functionality.
        """
        # This would need to be implemented based on a separate API endpoint
        # if available, or could be removed if not supported by the API
        raise NotImplementedError(
            "Message listing is not supported by the current API. "
            "Use get_senders() or get_available_numbers() instead."
        )

    def cancel(self, message_id: str) -> dict:
        """
        Legacy method for canceling messages (backward compatibility).

        Args:
            message_id: The message ID to cancel

        Returns:
            dict: Cancellation result

        Note:
            This method provides basic compatibility but may not be
            supported by the current API.
        """
        # This would need to be implemented based on a separate API endpoint
        # if available, or could be removed if not supported by the API
        raise NotImplementedError("Message cancellation is not supported by the current API.")
