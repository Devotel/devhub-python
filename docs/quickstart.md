# Quick Start

This guide will help you get started with the DevHub Python SDK.

## Installation

Install the SDK using pip:

```bash
pip install devhub-python
```

## Authentication

Initialize the client with your API key:

```python
from devhub_python import DevoClient

client = DevoClient(api_key="your-api-key")
```

!!! tip "Getting Your API Key"
    You can get your API key from the Devo dashboard after creating an account.

## Your First Message

### Send an SMS

```python
sms_response = client.sms.send_sms(
    recipient="+1234567890",
    message="Hello from DevHub SDK!",
    sender="+1987654321"
)
print(f"SMS sent with ID: {sms_response.id}")
```

### Send an Email

```python
email_response = client.email.send_email(
    recipient="user@example.com",
    subject="Welcome!",
    content="Thank you for using DevHub SDK.",
    sender_email="welcome@example.com"
)
print(f"Email sent with ID: {email_response.id}")
```

### Send a WhatsApp Message

```python
whatsapp_response = client.whatsapp.send_text_message(
    recipient="+1234567890",
    message="Hello via WhatsApp!"
)
print(f"WhatsApp message sent with ID: {whatsapp_response.id}")
```

## Error Handling

Always wrap your API calls in try-catch blocks:

```python
from devhub_python.exceptions import DevoException

try:
    sms_response = client.sms.send_sms(
        recipient="+1234567890",
        message="Hello!",
        sender="+1987654321"
    )
    print(f"Success: {sms_response.id}")
except DevoException as e:
    print(f"Error: {e}")
```

## Next Steps

- Explore the [SDK Reference](sdk/sms.md) for detailed usage
- Check out more [Examples](examples.md)
- Learn about [Error Handling](error_handling.md)
