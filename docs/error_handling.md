# Error Handling

The DevHub SDK provides comprehensive error handling to help you build robust applications.

## Exception Types

The SDK uses a hierarchy of exceptions for different error scenarios:

```python
from devhub_python.exceptions import DevoException
```

All SDK exceptions inherit from `DevoException`, making it easy to catch any SDK-related error.

## Basic Error Handling

### Simple Try-Catch

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

### Checking Response Status

```python
# Some API responses include status information
sms_response = client.sms.send_sms(
    recipient="+1234567890",
    message="Hello!",
    sender="+1987654321"
)

# Check if the response indicates an error
if hasattr(sms_response, 'is_error') and sms_response.is_error():
    print(f"API returned error: {sms_response.statusCode}")
else:
    print(f"Message sent successfully: {sms_response.id}")
```

## Common Error Scenarios

### Invalid Phone Numbers

```python
try:
    response = client.sms.send_sms(
        recipient="invalid-number",  # Invalid format
        message="Test",
        sender="+1987654321"
    )
except DevoException as e:
    print(f"Invalid phone number: {e}")
```

### Authentication Errors

```python
# Wrong API key
client = DevoClient(api_key="invalid-key")

try:
    response = client.sms.send_sms(
        recipient="+1234567890",
        message="Test",
        sender="+1987654321"
    )
except DevoException as e:
    print(f"Authentication failed: {e}")
```

### Missing Required Fields

```python
from devhub_python.models.contacts import CreateContactDto

try:
    # Missing required data
    contact_data = CreateContactDto()  # No required fields
    contact = client.services.contacts.create(contact_data)
except DevoException as e:
    print(f"Validation error: {e}")
```

## Retry Logic

### Simple Retry Pattern

```python
import time
from devhub_python.exceptions import DevoException

def send_with_retry(client, recipient, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.sms.send_sms(
                recipient=recipient,
                message=message,
                sender="+1987654321"
            )
        except DevoException as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                time.sleep(1)  # Wait 1 second before retry
                continue
            else:
                raise  # Re-raise the last exception
```

### Exponential Backoff

```python
import time
import random
from devhub_python.exceptions import DevoException

def send_with_backoff(client, recipient, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.sms.send_sms(
                recipient=recipient,
                message=message,
                sender="+1987654321"
            )
        except DevoException as e:
            if attempt < max_retries - 1:
                # Exponential backoff with jitter
                delay = (2 ** attempt) + random.uniform(0, 1)
                print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}")
                time.sleep(delay)
                continue
            else:
                raise
```

## Graceful Degradation

### Fallback to Alternative Channels

```python
from devhub_python.exceptions import DevoException

def send_message_with_fallback(client, recipient, message):
    """Try SMS first, fallback to WhatsApp if SMS fails."""

    # Try SMS first
    try:
        response = client.sms.send_sms(
            recipient=recipient,
            message=message,
            sender="+1987654321"
        )
        return {"channel": "sms", "response": response}

    except DevoException as sms_error:
        print(f"SMS failed: {sms_error}")

        # Fallback to WhatsApp
        try:
            response = client.whatsapp.send_text_message(
                recipient=recipient,
                message=message
            )
            return {"channel": "whatsapp", "response": response}

        except DevoException as whatsapp_error:
            print(f"WhatsApp also failed: {whatsapp_error}")
            raise DevoException("All channels failed") from whatsapp_error

# Usage
try:
    result = send_message_with_fallback(client, "+1234567890", "Important message!")
    print(f"Message sent via {result['channel']}: {result['response'].id}")
except DevoException as e:
    print(f"Could not send message: {e}")
```

## Logging Errors

### Basic Logging

```python
import logging
from devhub_python.exceptions import DevoException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message_with_logging(client, recipient, message):
    try:
        logger.info(f"Sending SMS to {recipient}")
        response = client.sms.send_sms(
            recipient=recipient,
            message=message,
            sender="+1987654321"
        )
        logger.info(f"SMS sent successfully: {response.id}")
        return response

    except DevoException as e:
        logger.error(f"SMS sending failed: {e}", exc_info=True)
        raise
```

## Best Practices

### 1. Always Use Try-Catch

```python
# Good
try:
    response = client.sms.send_sms(recipient, message, sender)
except DevoException as e:
    handle_error(e)

# Bad - no error handling
response = client.sms.send_sms(recipient, message, sender)
```

### 2. Validate Input Early

```python
def send_sms_safe(client, recipient, message, sender):
    # Validate inputs before making API call
    if not recipient or not recipient.startswith('+'):
        raise ValueError("Recipient must be in E.164 format")

    if not message or len(message.strip()) == 0:
        raise ValueError("Message cannot be empty")

    if not sender or not sender.startswith('+'):
        raise ValueError("Sender must be in E.164 format")

    try:
        return client.sms.send_sms(recipient, message, sender)
    except DevoException as e:
        logger.error(f"SMS API error: {e}")
        raise
```

### 3. Handle Partial Failures

```python
def send_bulk_messages(client, recipients, message):
    results = []
    failed = []

    for recipient in recipients:
        try:
            response = client.sms.send_sms(recipient, message, "+1987654321")
            results.append({"recipient": recipient, "status": "success", "id": response.id})
        except DevoException as e:
            failed.append({"recipient": recipient, "error": str(e)})

    return {
        "successful": results,
        "failed": failed,
        "total": len(recipients),
        "success_rate": len(results) / len(recipients)
    }
```

!!! warning "Rate Limits"
    Be mindful of API rate limits when implementing retry logic. Use exponential backoff to avoid overwhelming the API.
