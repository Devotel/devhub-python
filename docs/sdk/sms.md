# SMS

The SMS resource allows you to send text messages and manage SMS-related functionality.

## Sending SMS

### Basic SMS

```python
sms_response = client.sms.send_sms(
    recipient="+1234567890",
    message="Your verification code is: 123456",
    sender="+1987654321"
)
print(f"SMS sent with ID: {sms_response.id}")
print(f"Status: {sms_response.status}")
```

### Response Structure

The `send_sms()` method returns an `SMSQuickSendResponse` object with the following key fields:

- `id`: Unique message identifier
- `status`: Message status
- `recipient`: Recipient phone number
- `sender_id`: Sender identifier
- `sent_date`: Date message was sent

## Getting Available Senders

```python
senders = client.sms.get_senders()
for sender in senders.senders:
    print(f"Sender: {sender.phone_number} (Type: {sender.type})")
```

## Getting Available Numbers

```python
numbers = client.sms.get_available_numbers(
    region="US",
    type="mobile",
    limit=5
)
print(f"Found {len(numbers.numbers)} available numbers")

for number_info in numbers.numbers:
    if number_info.features:
        for feature in number_info.features:
            print(f"Number: {feature.phone_number}")
            print(f"Region: {feature.region_information}")
            print(f"Cost: {feature.cost_information}")
```

## Error Handling

```python
from devhub_python.exceptions import DevoException

try:
    sms_response = client.sms.send_sms(
        recipient="+1234567890",
        message="Test message",
        sender="+1987654321"
    )
except DevoException as e:
    print(f"SMS sending failed: {e}")
```

!!! note "Phone Number Format"
    All phone numbers must be in E.164 format (starting with +).
