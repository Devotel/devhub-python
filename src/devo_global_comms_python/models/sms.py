from datetime import datetime
from typing import Any, Dict, List, Optional

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
    hirvalidation: bool = Field(True, description="Enable HIR validation")


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

    id: str = Field(..., description="Unique message identifier")
    user_id: str = Field(..., description="User identifier")
    tenant_id: str = Field(..., description="Tenant identifier")
    sender_id: str = Field(..., description="Sender identifier")
    recipient: str = Field(..., description="Recipient phone number")
    message: str = Field(..., description="Message content")
    account_id: str = Field(..., description="Account identifier")
    account_type: str = Field(..., description="Account type")
    status: str = Field(..., description="Message status")
    message_timeline: Dict[str, Any] = Field(default_factory=dict, description="Message timeline events")
    message_id: str = Field(..., description="Message identifier")
    bulksmsid: str = Field(..., description="Bulk SMS identifier")
    sent_date: str = Field(..., description="Date message was sent")
    direction: str = Field(..., description="Message direction")
    recipientcontactid: str = Field(..., description="Recipient contact identifier")
    api_route: str = Field(..., description="API route used")
    apimode: str = Field(..., description="API mode")
    quicksendidentifier: str = Field(..., description="Quick send identifier")
    hirvalidation: bool = Field(..., description="HIR validation enabled")


class SenderInfo(BaseModel):
    """
    Model for sender information.
    """

    id: str = Field(..., description="Sender identifier")
    sender_id: str = Field(..., description="Sender ID")
    gateways_id: str = Field(..., description="Gateway identifier")
    phone_number: str = Field(..., description="Phone number")
    number: str = Field(..., description="Number")
    istest: bool = Field(..., description="Whether this is a test sender")
    type: str = Field(..., description="Sender type")


class SendersListResponse(BaseModel):
    """
    Response model for getting senders list.

    Returned from GET /user-api/me/senders
    """

    senders: List[SenderInfo] = Field(default_factory=list, description="List of available senders")


class RegionInformation(BaseModel):
    """
    Model for region information.
    """

    region_type: str = Field(..., description="Type of region")
    region_name: str = Field(..., description="Name of the region")


class CostInformation(BaseModel):
    """
    Model for cost information.
    """

    monthly_cost: str = Field(..., description="Monthly cost")
    setup_cost: str = Field(..., description="Setup cost")
    currency: str = Field(..., description="Currency code")


class NumberFeature(BaseModel):
    """
    Model for number feature information.
    """

    name: str = Field(..., description="Feature name")
    reservable: bool = Field(..., description="Whether the number is reservable")
    region_id: str = Field(..., description="Region identifier")
    number_type: str = Field(..., description="Type of number")
    quickship: bool = Field(..., description="Whether quickship is available")
    region_information: RegionInformation = Field(..., description="Region details")
    phone_number: str = Field(..., description="Phone number")
    cost_information: CostInformation = Field(..., description="Cost details")
    best_effort: bool = Field(..., description="Whether this is best effort")
    number_provider_type: str = Field(..., description="Number provider type")


class NumberPurchaseResponse(BaseModel):
    """
    Response model for number purchase API.

    Returned from POST /user-api/numbers/buy
    """

    features: List[NumberFeature] = Field(default_factory=list, description="List of number features")


class NumberInfo(BaseModel):
    """
    Model for number information in available numbers response.
    """

    features: List[NumberFeature] = Field(default_factory=list, description="List of features for this number")


class AvailableNumbersResponse(BaseModel):
    """
    Response model for available numbers API.

    Returned from GET /user-api/numbers
    """

    numbers: List[NumberInfo] = Field(default_factory=list, description="List of available numbers")


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
