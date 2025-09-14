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
        sandbox: bool = False,
    ) -> "SMSQuickSendResponse":
        """
        Send an SMS message using the quick-send API.

        Args:
            recipient: The recipient's phone number in E.164 format
            message: The SMS message content
            sender: The sender phone number or sender ID
            hirvalidation: Enable HIR validation (default: True)
            sandbox: Use sandbox environment for testing (default: False)

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
        response = self.client.post("user-api/sms/quick-send", json=request_data.dict(), sandbox=sandbox)

        # Parse response according to API spec
        from ..models.sms import SMSQuickSendResponse

        result = SMSQuickSendResponse.model_validate(response.json())
        logger.info(f"SMS sent successfully with ID: {result.id}")

        return result

    def get_senders(self, sandbox: bool = False) -> "SendersListResponse":
        """
        Retrieve the list of available senders for the account.

        Args:
            sandbox: Use sandbox environment for testing (default: False)

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
        response = self.client.get("user-api/me/senders", sandbox=sandbox)

        # Parse response according to API spec
        from ..models.sms import SendersListResponse

        result = SendersListResponse.model_validate(response.json())
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
        sandbox: bool = False,
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
            sandbox: Use sandbox environment for testing (default: False)

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

        result = NumberPurchaseResponse.model_validate(response.json())
        feature_count = len(result.features) if result.features else 0
        logger.info(f"Number purchased successfully with {feature_count} features")

        return result

    def get_available_numbers(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        capabilities: Optional[List[str]] = None,
        type: Optional[str] = None,
        prefix: Optional[str] = None,
        region: str = "US",
        sandbox: bool = False,
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
            sandbox: Use sandbox environment for testing (default: False)

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

        # Parse response according to API spec - API returns direct array
        from ..models.sms import AvailableNumbersResponse

        response_data = response.json()
        if isinstance(response_data, list):
            # API returns direct array, use custom parser
            result = AvailableNumbersResponse.parse_from_list(response_data)
        else:
            # Fallback to normal parsing if API changes
            result = AvailableNumbersResponse.model_validate(response_data)

        logger.info(f"Retrieved {len(result.numbers)} available numbers")

        return result

    # Legacy methods for backward compatibility
    def send(
        self, to: str, body: str, from_: Optional[str] = None, sandbox: bool = False, **kwargs
    ) -> "SMSQuickSendResponse":
        """
        Legacy method for sending SMS (backward compatibility).

        Args:
            to: The recipient's phone number in E.164 format
            body: The message body text
            from_: The sender's phone number (optional)
            sandbox: Use sandbox environment for testing (default: False)
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
