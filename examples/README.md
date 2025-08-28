# Devo Global Communications SDK - Examples

This directory contains comprehensive examples for using the Devo Global Communications SDK. Each resource has its own dedicated example file with detailed demonstrations of the available functionality.

## 📁 Example Files

### 🚀 Overview
- **`basic_usage.py`** - Interactive overview and launcher for all examples
- **`omni_channel_example.py`** - ✅ **Complete Omni-channel Messaging** - Unified API for all channels

### 📱 Communication Resources
- **`sms_example.py`** - ✅ **Complete SMS API implementation**
  - Send SMS messages via quick-send API
  - Get available senders
  - Search and purchase phone numbers
  - Legacy compatibility methods

- **`rcs_example.py`** - ✅ **Complete RCS API implementation**
  - Account management and messaging operations
  - Template and brand management
  - Tester management and capability testing
  - Rich messaging features (cards, carousels, suggestions)

- **`email_example.py`** - 🚧 **Placeholder** (Email functionality)
- **`whatsapp_example.py`** - 🚧 **Placeholder** (WhatsApp functionality)

### 👥 Management Resources
- **`contacts_example.py`** - 🚧 **Placeholder** (Contact management)
- **`contact_groups_example.py`** - ✅ **Complete Contact Groups API implementation**
  - CRUD operations for contact groups
  - Bulk operations and contact transfer
  - Search and pagination features
  - Metadata management and workflow examples

## 🚀 Getting Started

### Prerequisites
1. **API Key**: Get your API key from the Devo dashboard
2. **Environment**: Set the `DEVO_API_KEY` environment variable
   ```bash
   # Windows (PowerShell)
   $env:DEVO_API_KEY = "your_api_key_here"

   # Windows (Command Prompt)
   set DEVO_API_KEY=your_api_key_here

   # Unix/Linux/macOS
   export DEVO_API_KEY=your_api_key_here
   ```

### Running Examples

#### Option 1: Interactive Overview (Recommended)
```bash
python examples/basic_usage.py
```
This provides an interactive menu to choose and run specific examples.

#### Option 2: Run Individual Examples
```bash
# Omni-channel messaging (fully implemented)
python examples/omni_channel_example.py

# SMS functionality (fully implemented)
python examples/sms_example.py

# RCS functionality (fully implemented)
python examples/rcs_example.py

# Other resources (placeholder examples)
python examples/email_example.py
python examples/whatsapp_example.py
python examples/contacts_example.py

# Contact groups functionality (fully implemented)
python examples/contact_groups_example.py
```

## 🌐 Omni-channel Messaging Examples (Fully Implemented)

The unified messaging resource provides a single API endpoint to send messages through any channel:

### 🔧 Available Functions
1. **Send Message** - `client.messages.send()`
   - Uses POST `/api/v1/user-api/messages/send`
   - Supports SMS, Email, WhatsApp, and RCS channels
   - Channel-specific payload flexibility
   - Unified response format

### 💡 Key Features
- **Unified Interface**: One endpoint for all channels
- **Channel-specific Payloads**: Flexible payload structure for each channel
- **Type Safety**: Full Pydantic model validation
- **Metadata Support**: Custom metadata and webhook URLs
- **Bulk Messaging**: Easy iteration across multiple channels

### 📝 Example Usage
```python
from devo_global_comms_python.models.messages import SendMessageDto

# Send SMS
sms_data = SendMessageDto(
    channel="sms",
    to="+1234567890",
    payload={"text": "Hello World"}
)
result = client.messages.send(sms_data)

# Send Email
email_data = SendMessageDto(
    channel="email",
    to="user@example.com",
    payload={
        "subject": "Test Email",
        "text": "Hello World",
        "html": "<h1>Hello World</h1>"
    }
)
result = client.messages.send(email_data)
```

## 📱 SMS Examples (Fully Implemented)

The SMS resource is fully implemented with all four API endpoints:

### 🔧 Available Functions
1. **Send SMS** - `client.sms.send_sms()`
   - Uses POST `/user-api/sms/quick-send`
   - High-quality routing validation
   - Comprehensive response data

2. **Get Senders** - `client.sms.get_senders()`
   - Uses GET `/user-api/me/senders`
   - Lists all available sender numbers/IDs

3. **Search Numbers** - `client.sms.get_available_numbers()`
   - Uses GET `/user-api/numbers`
   - Filter by region, type, and limit results

4. **Purchase Numbers** - `client.sms.buy_number()`
   - Uses POST `/user-api/numbers/buy`
   - Complete number purchasing workflow

### 🔄 Legacy Compatibility
The SMS resource maintains backward compatibility with legacy methods while using the new API implementation underneath.

## 🚧 Placeholder Examples

The following examples show the structure and planned functionality but are not yet implemented:

- **Email**: Send emails, attachments, templates
- **WhatsApp**: Text messages, media, templates, business features
- **RCS**: Rich messaging, cards, carousels, capability checks
- **Contacts**: CRUD operations, contact management

## 📁 Contact Groups Examples (Fully Implemented)

The contact groups resource is fully implemented with all CRUD operations:

### 🔧 Available Functions
1. **List Groups** - `client.services.contact_groups.list()`
   - Uses GET `/api/v1/contacts-groups`
   - Pagination and search support
   - Field filtering capabilities

2. **Create Group** - `client.services.contact_groups.create()`
   - Uses POST `/api/v1/contacts-groups`
   - Metadata and contact assignment
   - Validation and error handling

3. **Update Group** - `client.services.contact_groups.update()`
   - Uses PUT `/api/v1/contacts-groups/{group_id}`
   - Partial updates with metadata
   - Flexible field modification

4. **Get Group** - `client.services.contact_groups.get_by_id()`
   - Uses GET `/api/v1/contacts-groups/{group_id}`
   - Complete group information retrieval

5. **Delete Group** - `client.services.contact_groups.delete_by_id()`
   - Uses DELETE `/api/v1/contacts-groups/{group_id}`
   - Individual group deletion with approval

6. **Bulk Delete** - `client.services.contact_groups.delete_bulk()`
   - Uses DELETE `/api/v1/contacts-groups`
   - Multiple group deletion with contact transfer

7. **Search Groups** - `client.services.contact_groups.search()`
   - Uses GET `/api/v1/contacts-groups`
   - Advanced search with field filtering

### 💡 Key Features
- **Complete CRUD Operations**: Full lifecycle management
- **Bulk Operations**: Efficient multi-group operations
- **Contact Transfer**: Safe deletion with contact preservation
- **Metadata Support**: Custom metadata for business logic
- **Search & Filter**: Advanced query capabilities
- **Pagination**: Efficient large dataset handling

### 📝 Example Usage
```python
from devo_global_comms_python.models.contact_groups import CreateContactsGroupDto

# Create new contact group (using new services namespace)
group_data = CreateContactsGroupDto(
    name="VIP Customers",
    description="High-value customers",
    contact_ids=["contact1", "contact2"],
    metadata={"priority": "high"}
)
group = client.services.contact_groups.create(group_data)

# List with pagination
groups = client.services.contact_groups.list(page=1, limit=10, search="VIP")

# Search groups
search_results = client.services.contact_groups.search(
    query="priority",
    fields=["name", "description"]
)

# Backward compatibility (deprecated - shows warning)
# groups = client.contact_groups.list()  # Still works but deprecated
```

## 🔧 Configuration Notes

### Phone Numbers
- Replace placeholder phone numbers (`+1234567890`) with actual numbers
- Ensure phone numbers are in E.164 format (e.g., `+1234567890`)
- Use valid sender numbers from your Devo dashboard

### Testing vs Production
- Some examples include test mode flags
- Number purchase examples are commented out to prevent accidental charges
- Always test with small limits when exploring available numbers

### Error Handling
All examples include comprehensive error handling with:
- Detailed error messages
- HTTP status codes
- API-specific error codes
- Response data debugging

## 🆔 Authentication

All examples use API key authentication:
```python
from devo_global_comms_python import DevoClient

client = DevoClient(api_key="your_api_key_here")
```

## 📋 Example Output

### SMS Example Output
```
📱 SMS QUICK-SEND API EXAMPLE
------------------------------
📤 Sending SMS to +1234567890...
✅ SMS sent successfully!
   📋 Message ID: msg_123456789
   📊 Status: sent
   📱 Recipient: +1234567890
   🔄 Direction: outbound

👥 GET AVAILABLE SENDERS EXAMPLE
------------------------------
✅ Found 3 available senders:
   1. 📞 Phone: +0987654321
      🏷️  Type: longcode
      🧪 Test Mode: No
```

## 🤝 Contributing

When implementing new resources:

1. **Create Resource Example**: Copy the structure from `sms_example.py`
2. **Update Basic Usage**: Add the new resource to `basic_usage.py`
3. **Update This README**: Document the new functionality
4. **Follow Patterns**: Use consistent emoji, formatting, and error handling

## 📚 Additional Resources

- **SDK Documentation**: [Link to main documentation]
- **API Reference**: [Link to API docs]
- **Devo Dashboard**: [Link to dashboard]
- **Support**: [Link to support]

---

**Need help?** Check the individual example files for detailed comments and error handling patterns.
