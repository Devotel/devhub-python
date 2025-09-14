from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import DevoClient


class BaseResource(ABC):
    """Base class for all API resources."""

    def __init__(self, client: "DevoClient"):
        """
        Initialize the resource.

        Args:
            client: The Devo client instance
        """
        self.client = client

    def _build_url(self, *path_parts: str) -> str:
        """
        Build a URL path from components.

        Args:
            *path_parts: Path components to join

        Returns:
            str: The joined path
        """
        return "/".join(str(part).strip("/") for part in path_parts if part)
