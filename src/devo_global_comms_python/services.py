"""
Services namespace for organizing service-related resources.

This module provides a namespace for accessing service-related functionality
such as contact management, contact groups, and other data management services.
"""

from typing import TYPE_CHECKING

from .resources.contact_groups import ContactGroupsResource
from .resources.contacts import ContactsResource

if TYPE_CHECKING:
    from .client import DevoClient


class ServicesNamespace:
    """
    Namespace for accessing service-related resources.

    This namespace organizes service-related functionality separately from
    messaging resources, providing a clear conceptual separation between
    sending messages and managing data/services.

    Example:
        >>> client = DevoClient(api_key="your-api-key")
        >>> # Access contact groups through services namespace
        >>> groups = client.services.contact_groups.list()
        >>> # Access contacts through services namespace
        >>> contacts = client.services.contacts.list()
    """

    def __init__(self, client: "DevoClient"):
        """
        Initialize the services namespace.

        Args:
            client: The DevoClient instance
        """
        self._client = client

        # Initialize service resources
        self.contact_groups = ContactGroupsResource(client)
        self.contacts = ContactsResource(client)

        # Future service resources will be added here:
        # self.templates = TemplatesResource(client)
        # self.analytics = AnalyticsResource(client)
        # etc.

    def __repr__(self) -> str:
        """String representation of the services namespace."""
        return f"<ServicesNamespace for {self._client.__class__.__name__}>"
