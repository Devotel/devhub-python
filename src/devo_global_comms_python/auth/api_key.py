from abc import ABC, abstractmethod
from typing import Dict


class BaseAuth(ABC):
    """Base authentication class."""

    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        pass


class APIKeyAuth(BaseAuth):
    """
    API Key authentication.

    Adds the API key to the request headers as 'X-API-Key'.
    """

    def __init__(self, api_key: str):
        """
        Initialize API key authentication.

        Args:
            api_key: The API key for authentication
        """
        self.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers with API key."""
        return {"X-API-Key": self.api_key}
