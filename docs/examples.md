# Examples

This page contains practical examples to help you get started with the DevHub SDK.

## Complete Working Examples

For detailed, working examples of each feature, check out the `examples/` directory in the SDK repository:

- **SMS Example**: `examples/sms_example.py`
- **Email Example**: `examples/email_example.py`
- **WhatsApp Example**: `examples/whatsapp_example.py`
- **RCS Example**: `examples/rcs_example.py`
- **Contacts Example**: `examples/contacts_example.py`
- **Contact Groups Example**: `examples/contact_groups_example.py`

## Multi-Channel Messaging

### Send the Same Message Across All Channels

```python
from devhub_python import DevoClient
from devhub_python.exceptions import DevoException

client = DevoClient(api_key="your-api-key")
recipient = "+1234567890"
message = "Hello from DevHub SDK!"

# Send via SMS
try:
    sms = client.sms.send_sms(
        recipient=recipient,
        message=message,
        sender="+1987654321"
    )
    print(f"SMS sent: {sms.id}")
except DevoException as e:
    print(f"SMS failed: {e}")

# Send via WhatsApp
try:
    whatsapp = client.whatsapp.send_text_message(
        recipient=recipient,
        message=message
    )
    print(f"WhatsApp sent: {whatsapp.id}")
except DevoException as e:
    print(f"WhatsApp failed: {e}")

# Send via RCS
try:
    rcs = client.rcs.send_text(
        recipient=recipient,
        message=message
    )
    print(f"RCS sent: {rcs.id}")
except DevoException as e:
    print(f"RCS failed: {e}")
```

## Contact Management Workflow

### Complete Contact Lifecycle

```python
from devhub_python.models.contacts import CreateContactDto, UpdateContactDto
from devhub_python.models.contact_groups import CreateContactsGroupDto

# 1. Create a contact
contact_data = CreateContactDto(
    phone_number="+1234567890",
    email="customer@example.com",
    first_name="Jane",
    last_name="Smith",
    company="Example Corp"
)

contact = client.services.contacts.create(contact_data)
print(f"Created contact: {contact.id}")

# 2. Create a contact group
group_data = CreateContactsGroupDto(
    name="New Customers",
    description="Recently onboarded customers"
)

group = client.services.contact_groups.create(group_data)
print(f"Created group: {group.id}")

# 3. Add contact to group
from devhub_python.models.contacts import AssignToContactsGroupDto

assignment = AssignToContactsGroupDto(
    contact_ids=[contact.id],
    contacts_group_id=group.id
)

client.services.contacts.assign_to_group(assignment)
print("Contact added to group")

# 4. Send welcome message
welcome_sms = client.sms.send_sms(
    recipient=contact.phone_number,
    message=f"Welcome {contact.first_name}! Thanks for joining {group.name}.",
    sender="+1987654321"
)
print(f"Welcome SMS sent: {welcome_sms.id}")
```

## Error Handling Best Practices

### Robust Message Sending

```python
import time
from devhub_python.exceptions import DevoException

def send_message_with_retry(client, recipient, message, max_retries=3):
    """Send a message with retry logic."""

    for attempt in range(max_retries):
        try:
            # Try SMS first
            response = client.sms.send_sms(
                recipient=recipient,
                message=message,
                sender="+1987654321"
            )
            print(f"SMS sent successfully: {response.id}")
            return response

        except DevoException as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                # Wait before retrying
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                # Try alternative channel on final failure
                try:
                    response = client.whatsapp.send_text_message(
                        recipient=recipient,
                        message=message
                    )
                    print(f"Fallback WhatsApp sent: {response.id}")
                    return response
                except DevoException as fallback_error:
                    print(f"All channels failed: {fallback_error}")
                    raise

# Usage
response = send_message_with_retry(client, "+1234567890", "Important message!")
```

## Environment Configuration

### Using Environment Variables

```python
import os
from devhub_python import DevoClient

# Set environment variables
# export DEVO_API_KEY="your-api-key"
# export DEVO_DEFAULT_SENDER="+1987654321"

def create_client():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        raise ValueError("DEVO_API_KEY environment variable is required")

    return DevoClient(api_key=api_key)

def send_notification(recipient, message):
    client = create_client()
    default_sender = os.getenv("DEVO_DEFAULT_SENDER", "+1234567890")

    return client.sms.send_sms(
        recipient=recipient,
        message=message,
        sender=default_sender
    )

# Usage
response = send_notification("+1234567890", "Hello from environment config!")
```

!!! tip "Running Examples"
    All examples in the `examples/` directory can be run directly after setting your `DEVO_API_KEY` environment variable.
