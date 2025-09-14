# Email

The Email resource allows you to send email messages using various methods.

## Sending Email

### Basic Email

```python
email_response = client.email.send_email(
    recipient="user@example.com",
    subject="Welcome to Devo!",
    content="Thank you for signing up for our service.",
    sender_email="welcome@example.com"
)
print(f"Email sent with ID: {email_response.id}")
```

### Template Email

```python
template_response = client.email.send_template_email(
    recipient="user@example.com",
    template_id="welcome_template",
    template_data={"name": "John", "company": "Acme Corp"},
    sender_email="noreply@example.com"
)
print(f"Template email sent with ID: {template_response.id}")
```

## Response Structure

Email methods return response objects with fields like:

- `id`: Unique email identifier
- `status`: Email status
- `recipient`: Recipient email address
- `sender_email`: Sender email address
- `subject`: Email subject line

## Error Handling

```python
from devhub_python.exceptions import DevoException

try:
    email_response = client.email.send_email(
        recipient="user@example.com",
        subject="Test",
        content="Test message",
        sender_email="test@example.com"
    )
except DevoException as e:
    print(f"Email sending failed: {e}")
```

!!! tip "Email Templates"
    Using templates allows for consistent branding and easier content management.
