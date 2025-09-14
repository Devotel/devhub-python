# DevHub Python SDK

[![PyPI version](https://badge.fury.io/py/devhub-python.svg)](https://badge.fury.io/py/devhub-python)
[![Python Support](https://img.shields.io/pypi/pyversions/devhub-python.svg)](https://pypi.org/project/devhub-python/)
[![Documentation](https://img.shields.io/badge/docs-github%20pages-blue)](https://devotel.github.io/devhub-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for the DevHub API, supporting SMS, Email, WhatsApp, RCS, and Contact management.

## Features

- **Multi-channel communication**: SMS, Email, WhatsApp, RCS
- **Contact management**: Create, update, and manage contacts
- **Unified messaging**: View and manage messages across all channels
- **Sync-first design**: Simple, blocking API calls
- **Type safety**: Full Pydantic model support with type hints
- **Minimal dependencies**: Only requires `requests` and `pydantic`
- **Python 3.8+ support**: Compatible with modern Python versions

## Installation

```bash
pip install devhub-python
```

## Quick Start

```python
from devhub_python import DevoClient

# Initialize the client
client = DevoClient(api_key="your-api-key")

# Send an SMS
sms_response = client.sms.send_sms(
    recipient="+1234567890",
    message="Hello, World!",
    sender="+1987654321"
)
print(f"SMS sent with ID: {sms_response.id}")

# Send an email
email_response = client.email.send_email(
    recipient="recipient@example.com",
    subject="Hello from Devo!",
    content="This is a test email from the Devo SDK.",
    sender_email="sender@example.com"
)
print(f"Email sent with ID: {email_response.id}")

# Send a WhatsApp message
whatsapp_response = client.whatsapp.send_text_message(
    recipient="+1234567890",
    message="Hello via WhatsApp!"
)
print(f"WhatsApp message sent with ID: {whatsapp_response.id}")
```

## Authentication

The SDK uses API key authentication:

```python
from devhub_python import DevoClient

client = DevoClient(api_key="your-api-key")
```

## Configuration

### Client Configuration

```python
client = DevoClient(
    api_key="your-api-key",
    timeout=30.0,  # Optional: request timeout
)
```

### Custom Session

You can provide your own `requests.Session` for advanced configuration:

```python
import requests
from devhub_python import DevoClient

session = requests.Session()
session.proxies = {"https": "https://proxy.example.com:8080"}

client = DevoClient(
    api_key="your-api-key",
    session=session
)
```

## Models

All API responses are returned as Pydantic models with full type support. The SDK includes models for:

- **SMS**: `SMSQuickSendResponse`, `SenderInfo`, `AvailableNumber`
- **Email**: `EmailSendResponse`, `EmailTemplateResponse`
- **WhatsApp**: `WhatsAppTextResponse`, `WhatsAppMediaResponse`
- **RCS**: `RCSMessage`, `RcsSendMessageSerializer`
- **Contacts**: `ContactSerializer`, `CreateContactDto`, `UpdateContactDto`
- **Contact Groups**: `ContactsGroup`, `CreateContactsGroupDto`

Example usage:
```python
# All responses are typed Pydantic models
sms_response = client.sms.send_sms(recipient="+1234567890", message="Hello", sender="+1987654321")
print(f"Message ID: {sms_response.id}")  # Type-safe access
print(f"Status: {sms_response.status}")
```

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/devotel/devhub-python.git
cd devhub-python

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/devhub_python

# Run specific test file
pytest tests/test_sms.py
```

### Code formatting

```bash
# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Run type checking with mypy
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://devotel.github.io/devhub-python/](https://devotel.github.io/devhub-python/)
- **Issues**: [GitHub Issues](https://github.com/devotel/devhub-python/issues)
- **Email**: [support@devotel.io](mailto:support@devotel.io)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for details about changes in each version.
