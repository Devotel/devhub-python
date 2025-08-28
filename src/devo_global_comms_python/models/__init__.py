from .contacts import Contact
from .email import EmailMessage
from .messages import Message, SendMessageDto, SendMessageSerializer
from .rcs import RCSMessage
from .sms import (
    AvailableNumbersResponse,
    CostInformation,
    NumberFeature,
    NumberInfo,
    NumberPurchaseRequest,
    NumberPurchaseResponse,
    RegionInformation,
    SenderInfo,
    SendersListResponse,
    SMSMessage,
    SMSQuickSendRequest,
    SMSQuickSendResponse,
)
from .whatsapp import WhatsAppMessage

__all__ = [
    # Legacy models
    "SMSMessage",
    "EmailMessage",
    "WhatsAppMessage",
    "RCSMessage",
    "Contact",
    "Message",
    # Omni-channel messaging models
    "SendMessageDto",
    "SendMessageSerializer",
    # New SMS API models
    "SMSQuickSendRequest",
    "SMSQuickSendResponse",
    "NumberPurchaseRequest",
    "NumberPurchaseResponse",
    "SendersListResponse",
    "SenderInfo",
    "AvailableNumbersResponse",
    "NumberInfo",
    "NumberFeature",
    "RegionInformation",
    "CostInformation",
]
