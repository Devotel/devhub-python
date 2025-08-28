from unittest.mock import Mock

import pytest

from devo_global_comms_python import DevoClient


@pytest.fixture
def mock_client():
    """Create a mock DevoClient for testing."""
    client = Mock(spec=DevoClient)
    client.base_url = "https://global-api-development.devotel.io/api/v1"
    client.timeout = 30.0
    return client


@pytest.fixture
def api_key():
    """Test API key."""
    return "test_api_key_12345"


@pytest.fixture
def test_phone_number():
    """Test phone number in E.164 format."""
    return "+1234567890"


@pytest.fixture
def test_email():
    """Test email address."""
    return "test@example.com"
