# RCS

The RCS (Rich Communication Services) resource allows you to send enhanced messages with rich media and interactive elements.

## Sending RCS Messages

### Text Message

```python
message = client.rcs.send_text(
    recipient="+1234567890",
    message="Hello from RCS!"
)
print(f"RCS message sent with ID: {message.id}")
```

### Rich Card Message

```python
rich_card = client.rcs.send_rich_card(
    recipient="+1234567890",
    title="Special Offer",
    description="Get 50% off your next purchase!",
    media_url="https://example.com/image.jpg"
)
print(f"Rich card sent with ID: {rich_card.id}")
```

### General Message (Alternative API)

```python
# Using the general send_message method
from devhub_python.models.rcs import RcsSendMessageSerializer

message_data = RcsSendMessageSerializer(
    recipient="+1234567890",
    message="Hello via general API!"
)

response = client.rcs.send_message(message_data)
print(f"Message sent with ID: {response.id}")
```

## Listing Messages

```python
messages = client.rcs.list_messages(limit=10)
print(f"Found {len(messages)} RCS messages")

for message in messages:
    print(f"Message ID: {message.id}")
    print(f"Status: {message.status}")
    print(f"Date: {message.date_created}")
```

## Response Structure

RCS methods return response objects with fields like:

- `id`: Unique message identifier
- `status`: Message status
- `recipient`: Recipient phone number
- `date_created`: Message creation timestamp
- `date_sent`: Message sent timestamp

## Error Handling

```python
from devhub_python.exceptions import DevoException

try:
    message = client.rcs.send_text(
        recipient="+1234567890",
        message="Hello!"
    )
except DevoException as e:
    print(f"RCS message failed: {e}")
```

!!! info "RCS Capabilities"
    RCS supports rich media, read receipts, typing indicators, and interactive elements like buttons and carousels.
