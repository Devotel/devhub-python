# WhatsApp

The WhatsApp resource enables sending messages through WhatsApp Business API.

## Sending Messages

### Text Message

```python
message = client.whatsapp.send_text_message(
    recipient="+1234567890",
    message="Hello from WhatsApp!"
)
print(f"Message sent with ID: {message.id}")
```

### Media Message

```python
media_message = client.whatsapp.send_media_message(
    recipient="+1234567890",
    media_url="https://example.com/image.jpg",
    media_type="image",
    caption="Check out this image!"
)
print(f"Media message sent with ID: {media_message.id}")
```

## Response Structure

WhatsApp methods return response objects with fields like:

- `id`: Unique message identifier
- `status`: Message status
- `recipient`: Recipient phone number
- `message_type`: Type of message sent
- `sent_date`: When the message was sent

## Error Handling

```python
from devhub_python.exceptions import DevoException

try:
    message = client.whatsapp.send_text_message(
        recipient="+1234567890",
        message="Hello!"
    )
except DevoException as e:
    print(f"WhatsApp message failed: {e}")
```

!!! note "WhatsApp Requirements"
    - Recipients must have opted-in to receive WhatsApp messages
    - Phone numbers must be in E.164 format
    - Media files must be accessible via public URLs
