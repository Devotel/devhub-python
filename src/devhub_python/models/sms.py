from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


# Request Models
class SMSQuickSendRequest(BaseModel):
    """
    Request model for SMS quick send API.

    Used for POST /user-api/sms/quick-send
    """

    sender: str = Field(..., description="Sender phone number or ID")
    recipient: str = Field(..., description="Recipient phone number in E.164 format")
    message: str = Field(..., description="SMS message content")
    hlrvalidation: bool = Field(True, description="Enable HIR validation")


class NumberPurchaseRequest(BaseModel):
    """
    Request model for purchasing a phone number.

    Used for POST /user-api/numbers/buy
    """

    region: str = Field(..., description="Region/country code for the number")
    number: str = Field(..., description="Phone number to purchase")
    number_type: str = Field(..., description="Type of number (mobile, landline, etc.)")
    is_longcode: bool = Field(True, description="Whether this is a long code number")
    agreement_last_sent_date: Optional[datetime] = Field(None, description="Last date agreement was sent")
    agency_authorized_representative: str = Field(..., description="Name of authorized representative")
    agency_representative_email: str = Field(..., description="Email of authorized representative")
    is_automated_enabled: bool = Field(True, description="Whether automated messages are enabled")


# Response Models
class SMSQuickSendResponse(BaseModel):
    """
    Response model for SMS quick send API.

    Returned from POST /user-api/sms/quick-send
    """

    # Success response fields
    id: Optional[str] = Field(None, description="Unique message identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    tenant_id: Optional[str] = Field(None, description="Tenant identifier")
    sender_id: Optional[str] = Field(None, description="Sender identifier")
    recipient: Optional[str] = Field(None, description="Recipient phone number")
    message: Optional[str] = Field(None, description="Message content")
    account_id: Optional[str] = Field(None, description="Account identifier")
    account_type: Optional[str] = Field(None, description="Account type")
    status: Optional[str] = Field(None, description="Message status")
    message_timeline: Optional[Dict[str, Any]] = Field(None, description="Message timeline events")
    message_id: Optional[str] = Field(None, description="Message identifier")
    bulksmsid: Optional[str] = Field(None, description="Bulk SMS identifier")
    sent_date: Optional[str] = Field(None, description="Date message was sent")
    direction: Optional[str] = Field(None, description="Message direction")
    recipientcontactid: Optional[str] = Field(None, description="Recipient contact identifier")
    api_route: Optional[str] = Field(None, description="API route used")
    apimode: Optional[str] = Field(None, description="API mode")
    quicksendidentifier: Optional[str] = Field(None, description="Quick send identifier")
    hlrvalidation: Optional[bool] = Field(None, description="HIR validation enabled")

    # Error response fields
    statusCode: Optional[int] = Field(None, description="HTTP status code for errors")

    def is_error(self) -> bool:
        """Check if this response represents an error."""
        return self.statusCode is not None and self.statusCode >= 400


class SenderInfo(BaseModel):
    """
    Model for sender information.
    """

    id: Optional[str] = Field(None, description="Sender identifier", alias="_id")
    sender_id: Optional[str] = Field(None, description="Sender ID")
    gateways_id: Optional[str] = Field(None, description="Gateway identifier")
    phone_number: Optional[str] = Field(None, description="Phone number")
    number: Optional[str] = Field(None, description="Number")
    istest: Optional[bool] = Field(None, description="Whether this is a test sender")
    type: str = Field(..., description="Sender type")

    # Additional fields found in actual API response
    name: Optional[str] = Field(None, description="Sender name")

    class Config:
        allow_population_by_field_name = True


class SendersListResponse(BaseModel):
    """
    Response model for getting senders list.

    Returned from GET /user-api/me/senders
    """

    senders: List[SenderInfo] = Field(default_factory=list, description="List of available senders")


class RegionInformation(BaseModel):
    """Model for region information."""

    region_type: Optional[str] = Field(None, description="Type of region")
    region_name: Optional[str] = Field(None, description="Name of the region")


class CostInformation(BaseModel):
    """Model for cost information."""

    monthly_cost: Optional[str] = Field(None, description="Monthly cost")
    setup_cost: Optional[str] = Field(None, description="Setup cost")
    currency: Optional[str] = Field(None, description="Currency code")


class PurchaseFeature(BaseModel):
    """Model for purchased number features."""

    name: Optional[str] = Field(None, description="Feature name")
    reservable: Optional[bool] = Field(None, description="Whether feature is reservable")
    region_id: Optional[str] = Field(None, description="Region ID")
    number_type: Optional[str] = Field(None, description="Number type")
    quickship: Optional[bool] = Field(None, description="Quickship availability")
    region_information: Optional[RegionInformation] = Field(None, description="Region information")
    phone_number: Optional[str] = Field(None, description="Phone number")
    cost_information: Optional[CostInformation] = Field(None, description="Cost information")
    best_effort: Optional[bool] = Field(None, description="Best effort flag")
    number_provider_type: Optional[str] = Field(None, description="Number provider type")


class AvailableNumberFeature(BaseModel):
    """Model for features available with a number."""

    name: Optional[str] = Field(None, description="Feature name")
    reservable: Optional[bool] = Field(None, description="Whether feature is reservable")
    region_id: Optional[str] = Field(None, description="Region ID")
    number_type: Optional[str] = Field(None, description="Number type")
    quickship: Optional[bool] = Field(None, description="Quickship availability")
    region_information: Optional[Any] = Field(None, description="Region information")
    phone_number: Optional[str] = Field(None, description="Phone number")
    cost_information: Optional[Any] = Field(None, description="Cost information")
    best_effort: Optional[bool] = Field(None, description="Best effort flag")
    number_provider_type: Optional[str] = Field(None, description="Number provider type")


class NumberFeature(BaseModel):
    """
    Model for number feature information.
    """

    name: str = Field(..., description="Feature name")


class NumberPurchaseResponse(BaseModel):
    """
    Response model for number purchase API.

    Returned from POST /user-api/numbers/buy
    """

    success: Optional[bool] = Field(None, description="Whether the purchase was successful")
    message: Optional[Union[str, List[str]]] = Field(None, description="Response message (can be string or array)")
    statusCode: Optional[int] = Field(None, description="HTTP status code")
    features: Optional[List[PurchaseFeature]] = Field(None, description="Features associated with the number")
    phone_number: Optional[str] = Field(None, description="Purchased phone number")
    id: Optional[str] = Field(None, alias="_id", description="Unique identifier for the purchased number")
    # Add other fields as discovered from actual API responses


# Legacy/compatibility classes
class NumberInfo(BaseModel):
    """
    Legacy model for number information in available numbers response.
    Kept for backward compatibility.
    """

    features: List[NumberFeature] = Field(default_factory=list, description="List of features for this number")


class AvailableNumber(BaseModel):
    """
    Model for individual available number information.
    """

    vanity_format: Optional[str] = Field(None, description="Vanity format if applicable")
    number_provider_type: Optional[Any] = Field(None, description="Number provider type identifier")
    reservable: Optional[bool] = Field(None, description="Whether the number is reservable")
    phone_number_type: Optional[str] = Field(None, description="Type of phone number")
    region_information: Optional[Any] = Field(None, description="Region details")
    quickship: Optional[bool] = Field(None, description="Whether quickship is available")
    phone_number: Optional[str] = Field(None, description="Phone number")
    cost_information: Optional[Any] = Field(None, description="Cost details")
    record_type: Optional[str] = Field(None, description="Record type")
    best_effort: Optional[bool] = Field(None, description="Whether this is best effort")
    features: Optional[List[AvailableNumberFeature]] = Field(None, description="Available features")
    carrier: Optional[str] = Field(None, description="Carrier name")


class AvailableNumbersResponse(BaseModel):
    """
    Response model for available numbers API.

    Returned from GET /user-api/numbers
    Note: The API returns a direct array, not a wrapped object
    """

    def __init__(self, data: List[Dict] = None, **kwargs):
        """Custom constructor to handle direct array response."""
        if data is not None and isinstance(data, list):
            # Convert list of dicts to list of AvailableNumber objects
            numbers = [AvailableNumber.model_validate(item) for item in data]
            super().__init__(numbers=numbers, **kwargs)
        else:
            super().__init__(**kwargs)

    numbers: List[AvailableNumber] = Field(default_factory=list, description="List of available numbers")

    @classmethod
    def parse_from_list(cls, data: List[Dict]) -> "AvailableNumbersResponse":
        """Parse from direct array response."""
        numbers = [AvailableNumber.model_validate(item) for item in data]
        return cls(numbers=numbers)


# Legacy model for backward compatibility
class SMSMessage(BaseModel):
    """
    Legacy SMS message model for backward compatibility.

    This model maintains compatibility with existing code while new code
    should use the specific request/response models above.
    """

    sid: str = Field(..., description="Unique identifier for the message")
    account_sid: Optional[str] = Field(None, description="Account identifier")
    to: str = Field(..., description="Recipient phone number in E.164 format")
    from_: Optional[str] = Field(None, alias="from", description="Sender phone number")
    body: str = Field(..., description="Message body text")
    status: str = Field(..., description="Message status")
    direction: str = Field(..., description="Message direction (inbound/outbound)")
    price: Optional[str] = Field(None, description="Message price")
    price_unit: Optional[str] = Field(None, description="Price currency unit")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    num_segments: Optional[int] = Field(None, description="Number of message segments")
    media_urls: Optional[List[str]] = Field(None, description="URLs of attached media")
    date_created: Optional[datetime] = Field(None, description="Message creation timestamp")
    date_sent: Optional[datetime] = Field(None, description="Message sent timestamp")
    date_updated: Optional[datetime] = Field(None, description="Message last updated timestamp")
    messaging_service_sid: Optional[str] = Field(None, description="Messaging service identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Custom metadata")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
