from .contact_groups import ContactGroupsResource
from .contacts import ContactsResource
from .email import EmailResource
from .messages import MessagesResource
from .rcs import RCSResource
from .sms import SMSResource
from .whatsapp import WhatsAppResource

__all__ = [
    "SMSResource",
    "EmailResource",
    "WhatsAppResource",
    "RCSResource",
    "ContactsResource",
    "ContactGroupsResource",
    "MessagesResource",
]
