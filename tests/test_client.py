from unittest.mock import Mock, patch

import pytest
import requests

from devo_global_comms_python import DevoClient
from devo_global_comms_python.exceptions import DevoAPIException, DevoAuthenticationException


class TestDevoClient:
    """Test cases for the DevoClient class."""

    def test_client_initialization_with_api_key(self, api_key):
        """Test client initialization with API key."""
        client = DevoClient(api_key=api_key)

        assert client.base_url == DevoClient.DEFAULT_BASE_URL
        assert client.timeout == DevoClient.DEFAULT_TIMEOUT
        assert client.auth.api_key == api_key

    def test_client_initialization_with_custom_params(self, api_key):
        """Test client initialization with custom parameters."""
        base_url = "https://custom.api.com"
        timeout = 60.0
        max_retries = 5

        client = DevoClient(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries)

        assert client.base_url == base_url
        assert client.timeout == timeout

    def test_client_has_all_resources(self, api_key):
        """Test that client has all expected resources."""
        client = DevoClient(api_key=api_key)

        assert hasattr(client, "sms")
        assert hasattr(client, "email")
        assert hasattr(client, "whatsapp")
        assert hasattr(client, "rcs")
        assert hasattr(client, "contacts")
        assert hasattr(client, "messages")

    @patch("requests.Session.request")
    def test_successful_request(self, mock_request, api_key):
        """Test successful API request."""
        # Setup mock response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = DevoClient(api_key=api_key)
        response = client.get("test/endpoint")

        assert response == mock_response
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_api_error_handling(self, mock_request, api_key):
        """Test API error handling."""
        # Setup mock error response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "message": "Bad Request",
            "code": "INVALID_PARAMS",
        }
        mock_request.return_value = mock_response

        client = DevoClient(api_key=api_key)

        with pytest.raises(DevoAPIException) as exc_info:
            client.get("test/endpoint")

        assert exc_info.value.status_code == 400
        assert "Bad Request" in str(exc_info.value)

    @patch("requests.Session.request")
    def test_authentication_error_handling(self, mock_request, api_key):
        """Test authentication error handling."""
        # Setup mock auth error response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Unauthorized"}
        mock_request.return_value = mock_response

        client = DevoClient(api_key=api_key)

        with pytest.raises(DevoAuthenticationException):
            client.get("test/endpoint")

    @patch("requests.Session.request")
    def test_timeout_error_handling(self, mock_request, api_key):
        """Test timeout error handling."""
        mock_request.side_effect = requests.exceptions.Timeout()

        client = DevoClient(api_key=api_key)

        with pytest.raises(Exception) as exc_info:
            client.get("test/endpoint")

        assert "timed out" in str(exc_info.value).lower()

    def test_http_methods(self, api_key):
        """Test HTTP method shortcuts."""
        client = DevoClient(api_key=api_key)

        with patch.object(client, "request") as mock_request:
            client.get("path")
            mock_request.assert_called_with("GET", "path")

            client.post("path", json={"data": "test"})
            mock_request.assert_called_with("POST", "path", json={"data": "test"})

            client.put("path")
            mock_request.assert_called_with("PUT", "path")

            client.delete("path")
            mock_request.assert_called_with("DELETE", "path")

            client.patch("path")
            mock_request.assert_called_with("PATCH", "path")
