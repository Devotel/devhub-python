from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import __version__
from .auth import APIKeyAuth
from .exceptions import DevoAPIException, DevoAuthenticationException, DevoException, DevoMissingAPIKeyException
from .resources.contacts import ContactsResource
from .resources.email import EmailResource
from .resources.messages import MessagesResource
from .resources.rcs import RCSResource
from .resources.sms import SMSResource
from .resources.whatsapp import WhatsAppResource
from .services import ServicesNamespace


class DevoClient:
    """
    Main client for interacting with the DevHub API.

    This client follows a resource-based pattern with two main namespaces:
    - Messaging resources: Direct access to communication channels (SMS, Email, etc.)
    - Services namespace: Organized access to data management services

    Example:
        >>> client = DevoClient(api_key="your-api-key")
        >>>
        >>> # Messaging resources (direct access)
        >>> response = client.sms.send_sms(
        ...     recipient="+1234567890",
        ...     message="Hello, World!",
        ...     sender="+0987654321"
        ... )
        >>> print(f"Message ID: {response.id}")
        >>>
        >>> # Services namespace (organized access)
        >>> groups = client.services.contact_groups.list()
        >>> for group in groups.groups:
        ...     print(f"Group: {group.name}")
        >>>
        >>> # Omni-channel messaging
        >>> from devhub_python.models.messages import SendMessageDto
        >>> message = client.messages.send(SendMessageDto(
        ...     channel="sms",
        ...     to="+1234567890",
        ...     payload={"text": "Hello World"}
        ... ))
    """

    DEFAULT_BASE_URL = "https://global-api-development.devotel.io/api/v1"
    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        api_key: str,
        sandbox_api_key: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the Devo client.

        Args:
            api_key: API key for authentication
            sandbox_api_key: Optional sandbox API key for testing environments
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            session: Custom requests session (optional)

        Raises:
            DevoMissingAPIKeyException: If API key is not provided
        """
        if not api_key or not api_key.strip():
            raise DevoMissingAPIKeyException()

        self.api_key = api_key.strip()
        self.sandbox_api_key = sandbox_api_key.strip() if sandbox_api_key else None
        self.base_url = self.DEFAULT_BASE_URL
        self.timeout = timeout

        # Set up authentication
        self.auth = APIKeyAuth(api_key.strip())

        # Set up session with retry strategy
        self.session = session or self._create_session(max_retries)

        # Initialize messaging resources
        self.sms = SMSResource(self)
        self.email = EmailResource(self)
        self.whatsapp = WhatsAppResource(self)
        self.rcs = RCSResource(self)
        self.contacts = ContactsResource(self)
        self.messages = MessagesResource(self)

        # Initialize services namespace
        self.services = ServicesNamespace(self)

    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        sandbox: bool = False,
    ) -> requests.Response:
        """
        Make an authenticated request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API endpoint path (without base URL)
            params: Query parameters
            data: Form data
            json: JSON data
            headers: Additional headers
            sandbox: Use sandbox API key for this request (default: False)

        Returns:
            requests.Response: The API response

        Raises:
            DevoAPIException: If the API returns an error
            DevoException: For other request errors
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

        # Validate sandbox usage
        if sandbox and not self.sandbox_api_key:
            raise DevoException("Sandbox API key required when sandbox=True")

        # Prepare headers
        request_headers = {
            "User-Agent": f"devo-python-sdk/{__version__}",
            "Accept": "application/json",
        }
        if headers:
            request_headers.update(headers)

        # Add authentication headers
        if sandbox and self.sandbox_api_key:
            # Use sandbox API key for this request
            sandbox_auth = APIKeyAuth(self.sandbox_api_key)
            auth_headers = sandbox_auth.get_headers()
        else:
            # Use regular API key
            auth_headers = self.auth.get_headers()
        request_headers.update(auth_headers)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=request_headers,
                timeout=self.timeout,
            )

            # Check for API errors
            if not response.ok:
                self._handle_error_response(response)

            return response

        except requests.exceptions.Timeout:
            raise DevoException("Request timed out")
        except requests.exceptions.ConnectionError:
            raise DevoException("Connection error")
        except requests.exceptions.RequestException as e:
            raise DevoException(f"Request failed: {str(e)}")

    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle error responses from the API."""
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown error")
            error_code = error_data.get("code")
        except ValueError:
            error_message = response.text or f"HTTP {response.status_code}"
            error_code = None

        if response.status_code == 401:
            raise DevoAuthenticationException(error_message)
        elif response.status_code == 429:
            from .exceptions import DevoRateLimitException

            raise DevoRateLimitException(error_message)
        else:
            raise DevoAPIException(
                message=error_message,
                status_code=response.status_code,
                error_code=error_code,
                response=response,
            )

    def get(self, path: str, **kwargs) -> requests.Response:
        """Make a GET request."""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """Make a POST request."""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """Make a PUT request."""
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """Make a DELETE request."""
        return self.request("DELETE", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        """Make a PATCH request."""
        return self.request("PATCH", path, **kwargs)
