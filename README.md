# Devo Global Communications Python SDK

[![PyPI version](https://badge.fury.io/py/devo-global-comms-python.svg)](https://badge.fury.io/py/devo-global-comms-python)
[![Python Support](https://img.shields.io/pypi/pyversions/devo-global-comms-python.svg)](https://pypi.org/project/devo-global-comms-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for the Devo Global Communications API, supporting SMS, Email, WhatsApp, RCS, and Contact management.

## Features

- **Multi-channel communication**: SMS, Email, WhatsApp, RCS
- **Contact management**: Create, update, and manage contacts
- **Unified messaging**: View and manage messages across all channels
- **Sync-first design**: Simple, blocking API calls
- **Type safety**: Full Pydantic model support with type hints
- **Minimal dependencies**: Only requires `requests` and `pydantic`
- **Resource-based pattern**: Familiar API design
- **Python 3.8+ support**: Compatible with modern Python versions

## Installation

```bash
pip install devo-global-comms-python
```

## Quick Start

```python
from devo_global_comms_python import DevoClient

# Initialize the client
client = DevoClient(api_key="your-api-key")

# Send an SMS
sms = client.sms.send(
    to="+1234567890",
    body="Hello, World!"
)
print(f"SMS sent with SID: {sms.sid}")

# Send an email
email = client.email.send(
    to="recipient@example.com",
    subject="Hello from Devo!",
    body="This is a test email from the Devo SDK."
)
print(f"Email sent with ID: {email.id}")

# Send a WhatsApp message
whatsapp = client.whatsapp.send_text(
    to="+1234567890",
    text="Hello via WhatsApp!"
)
print(f"WhatsApp message sent with ID: {whatsapp.id}")
```

## Authentication

The SDK uses API key authentication:

```python
from devo_global_comms_python import DevoClient

client = DevoClient(api_key="your-api-key")
```

## Usage Examples

### SMS Messages

```python
# Send a simple SMS
message = client.sms.send(
    to="+1234567890",
    body="Your verification code is: 123456"
)

# Send SMS with custom sender and callback
message = client.sms.send(
    to="+1234567890",
    body="Hello from Devo!",
    from_="+1987654321",
    callback_url="https://your-app.com/webhook",
    metadata={"campaign": "welcome_series"}
)

# Get message details
message = client.sms.get("message_sid")
print(f"Status: {message.status}")

# List recent messages
messages = client.sms.list(
    date_sent_after="2024-01-01",
    status="delivered",
    limit=10
)
```

### Email Messages

```python
# Send a simple email
email = client.email.send(
    to="user@example.com",
    subject="Welcome to Devo!",
    body="Thank you for signing up for our service."
)

# Send HTML email with CC and attachments
email = client.email.send(
    to="user@example.com",
    subject="Monthly Newsletter",
    body="Check out our latest updates!",
    html_body="<h1>Monthly Newsletter</h1><p>Check out our latest updates!</p>",
    cc=["manager@example.com"],
    reply_to="noreply@example.com",
    attachments=[
        {
            "filename": "newsletter.pdf",
            "content": "base64-encoded-content",
            "content_type": "application/pdf"
        }
    ]
)

# List emails by recipient
emails = client.email.list(
    to="user@example.com",
    limit=20
)
```

### WhatsApp Messages

```python
# Send a text message
message = client.whatsapp.send_text(
    to="+1234567890",
    text="Hello from WhatsApp!"
)

# Send a template message
message = client.whatsapp.send_template(
    to="+1234567890",
    template_name="welcome_message",
    language="en",
    parameters=["John", "Devo Platform"]
)

# Get message status
message = client.whatsapp.get("message_id")
print(f"Status: {message.status}")
```

### RCS Messages

```python
# Send a text message
message = client.rcs.send_text(
    to="+1234567890",
    text="Hello from RCS!"
)

# Send a rich card
message = client.rcs.send_rich_card(
    to="+1234567890",
    title="Special Offer",
    description="Get 50% off your next purchase!",
    media_url="https://example.com/image.jpg",
    actions=[
        {
            "type": "url",
            "text": "Shop Now",
            "url": "https://example.com/shop"
        }
    ]
)
```

### Contact Management

```python
# Create a contact
contact = client.contacts.create(
    phone_number="+1234567890",
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    company="Acme Corp",
    metadata={"source": "website_signup"}
)

# Update a contact
updated_contact = client.contacts.update(
    contact_id=contact.id,
    company="New Company Inc.",
    metadata={"updated": "2024-01-15"}
)

# Get contact details
contact = client.contacts.get("contact_id")

# List contacts
contacts = client.contacts.list(
    company="Acme Corp",
    limit=50
)

# Delete a contact
success = client.contacts.delete("contact_id")
```

### Unified Message Management

```python
# Get any message by ID
message = client.messages.get("message_id")
print(f"Channel: {message.channel}, Status: {message.status}")

# List messages across all channels
messages = client.messages.list(
    channel="sms",  # Filter by channel
    status="delivered",
    date_sent_after="2024-01-01",
    limit=100
)

# Get detailed delivery status
delivery_status = client.messages.get_delivery_status("message_id")

# Resend a failed message
resent_message = client.messages.resend("failed_message_id")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from devo_global_comms_python import (
    DevoException,
    DevoAPIException,
    DevoAuthenticationException,
    DevoValidationException,
    DevoRateLimitException,
    DevoTimeoutException,
)

try:
    message = client.sms.send(
        to="invalid-number",
        body="Test message"
    )
except DevoValidationException as e:
    print(f"Validation error: {e}")
except DevoAuthenticationException as e:
    print(f"Authentication failed: {e}")
except DevoRateLimitException as e:
    print(f"Rate limit exceeded. Retry after: {e.retry_after}")
except DevoAPIException as e:
    print(f"API error [{e.status_code}]: {e}")
except DevoException as e:
    print(f"General error: {e}")
```

## Configuration

### Client Configuration

```python
client = DevoClient(
    api_key="your-api-key",
    timeout=30.0,
    max_retries=3,
)
```

### Custom Session

You can provide your own `requests.Session` for advanced configuration:

```python
import requests
from devo_global_comms_python import DevoClient

session = requests.Session()
session.proxies = {"https": "https://proxy.example.com:8080"}

client = DevoClient(
    api_key="your-api-key",
    session=session
)
```

## Models

All API responses are returned as Pydantic models with full type support:

```python
# SMS Message model
class SMSMessage(BaseModel):
    sid: str
    to: str
    from_: Optional[str]
    body: str
    status: str
    date_created: Optional[datetime]
    # ... other fields

# Email Message model
class EmailMessage(BaseModel):
    id: str
    to: str
    subject: str
    body: str
    status: str
    # ... other fields

# Contact model
class Contact(BaseModel):
    id: str
    phone_number: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    # ... other fields
```

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/devotel/devo-global-comms-python.git
cd devo-global-comms-python

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
pytest --cov=src/devo_global_comms_python

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

- **Documentation**: [https://devo-global-comms-python.readthedocs.io](https://devo-global-comms-python.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/devotel/devo-global-comms-python/issues)
- **Email**: [support@devo.com](mailto:support@devo.com)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for details about changes in each version.
