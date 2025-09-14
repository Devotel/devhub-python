# DevHub Python SDK

A Python SDK for the DevHub API, supporting SMS, Email, WhatsApp, RCS, and Contact management.

## Features

- **Multi-channel communication**: SMS, Email, WhatsApp, RCS
- **Contact management**: Create, update, and manage contacts
- **Type safety**: Full Pydantic model support with type hints
- **Minimal dependencies**: Only requires `requests` and `pydantic`
- **Python 3.8+ support**: Compatible with modern Python versions

## Installation

```bash
pip install devhub-python
```

## Quick Example

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
```

## Getting Started

Continue to the [Quick Start](quickstart.md) guide to learn how to use the SDK.

## SDK Overview

The DevHub SDK is organized into logical resources:

| Resource | Purpose | Example Usage |
|----------|---------|---------------|
| **SMS** | Send text messages | `client.sms.send_sms()` |
| **Email** | Send emails | `client.email.send_email()` |
| **WhatsApp** | Send WhatsApp messages | `client.whatsapp.send_text_message()` |
| **RCS** | Send rich RCS messages | `client.rcs.send_text()` |
| **Contacts** | Manage contacts | `client.services.contacts.create()` |
| **Contact Groups** | Manage contact groups | `client.services.contact_groups.create()` |

## Support

- **Issues**: [GitHub Issues](https://github.com/devotel/devhub-python/issues)
- **Email**: [support@devotel.io](mailto:support@devotel.io)
