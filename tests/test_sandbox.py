#!/usr/bin/env python3
"""
Tests for sandbox functionality in the Devo Global Communications Python SDK.
"""

from unittest.mock import Mock, patch

import pytest

from devo_global_comms_python.client import DevoClient
from devo_global_comms_python.exceptions import DevoException


class TestSandboxFunctionality:
    """Test sandbox API key switching functionality."""

    def test_client_initialization_with_sandbox_api_key(self):
        """Test that client can be initialized with sandbox API key."""
        client = DevoClient(api_key="test-api-key", sandbox_api_key="sandbox-api-key")

        assert client.api_key == "test-api-key"
        assert client.sandbox_api_key == "sandbox-api-key"

    def test_client_initialization_without_sandbox_api_key(self):
        """Test that client can be initialized without sandbox API key."""
        client = DevoClient(api_key="test-api-key")

        assert client.api_key == "test-api-key"
        assert client.sandbox_api_key is None

    def test_sandbox_request_without_sandbox_api_key_raises_error(self):
        """Test that sandbox request without sandbox API key raises appropriate error."""
        client = DevoClient(api_key="test-api-key")

        with pytest.raises(DevoException, match="Sandbox API key required when sandbox=True"):
            client.get("test-endpoint", sandbox=True)

    @patch("devo_global_comms_python.client.requests.Session.request")
    def test_sandbox_request_uses_sandbox_api_key(self, mock_request):
        """Test that sandbox request uses sandbox API key for authentication."""
        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = DevoClient(api_key="production-api-key", sandbox_api_key="sandbox-api-key")

        # Make sandbox request
        client.get("test-endpoint", sandbox=True)

        # Verify the request was made with sandbox API key
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        headers = call_args[1]["headers"]

        # Check that X-API-Key header contains sandbox API key
        assert "X-API-Key" in headers
        assert "sandbox-api-key" in headers["X-API-Key"]

    @patch("devo_global_comms_python.client.requests.Session.request")
    def test_regular_request_uses_production_api_key(self, mock_request):
        """Test that regular request uses production API key for authentication."""
        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = DevoClient(api_key="production-api-key", sandbox_api_key="sandbox-api-key")

        # Make regular request (sandbox=False by default)
        client.get("test-endpoint")

        # Verify the request was made with production API key
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        headers = call_args[1]["headers"]

        # Check that X-API-Key header contains production API key
        assert "X-API-Key" in headers
        assert "production-api-key" in headers["X-API-Key"]

    @patch("devo_global_comms_python.client.requests.Session.request")
    def test_sms_resource_sandbox_parameter(self, mock_request):
        """Test that SMS resource functions correctly pass sandbox parameter."""
        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"senders": []}
        mock_request.return_value = mock_response

        client = DevoClient(api_key="production-api-key", sandbox_api_key="sandbox-api-key")

        # Call SMS function with sandbox=True
        client.sms.get_senders(sandbox=True)

        # Verify the request was made with sandbox API key
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        headers = call_args[1]["headers"]

        # Check that X-API-Key header contains sandbox API key
        assert "X-API-Key" in headers
        assert "sandbox-api-key" in headers["X-API-Key"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
