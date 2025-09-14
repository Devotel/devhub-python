# Contacts

The Contacts resource allows you to manage contact information through the services namespace.

## Creating Contacts

```python
from devhub_python.models.contacts import CreateContactDto

# Create a contact
contact_data = CreateContactDto(
    phone_number="+1234567890",
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    company="Acme Corp"
)

contact = client.services.contacts.create(contact_data)
print(f"Contact created with ID: {contact.id}")
```

## Listing Contacts

```python
# List contacts with pagination
contacts_response = client.services.contacts.list(page=1, limit=10)
print(f"Found {contacts_response.total} total contacts")
print(f"Page: {contacts_response.page}/{contacts_response.total_pages}")

for contact in contacts_response.contacts:
    name = f"{contact.first_name or ''} {contact.last_name or ''}".strip()
    print(f"Contact: {name} ({contact.email})")
```

## Updating Contacts

```python
from devhub_python.models.contacts import UpdateContactDto

# Update a contact
update_data = UpdateContactDto(
    company="New Company Inc.",
    tags=["updated", "important"]
)

updated_contact = client.services.contacts.update(contact.id, update_data)
print(f"Contact updated: {updated_contact.company}")
```

## Filtering Contacts

```python
# Search and filter contacts
filtered_contacts = client.services.contacts.list(
    page=1,
    limit=10,
    search="Acme",
    is_email_subscribed=True,
    tags=["customer"]
)
print(f"Found {filtered_contacts.total} contacts matching filters")
```

## Custom Fields

### Create Custom Field

```python
from devhub_python.models.contacts import CreateCustomFieldDto

field_data = CreateCustomFieldDto(
    name="Department",
    field_type="text",
    description="Employee department",
    is_required=False
)

new_field = client.services.contacts.create_custom_field(field_data)
print(f"Custom field created: {new_field.name}")
```

### List Custom Fields

```python
custom_fields = client.services.contacts.list_custom_fields(page=1, limit=5)
print(f"Found {custom_fields.total} custom fields")
```

## Contact Group Operations

### Assign to Group

```python
from devhub_python.models.contacts import AssignToContactsGroupDto

assignment_data = AssignToContactsGroupDto(
    contact_ids=[contact.id],
    contacts_group_id="group_id_123"
)

client.services.contacts.assign_to_group(assignment_data)
print("Contact assigned to group")
```

### Unassign from Group

```python
client.services.contacts.unassign_from_group(assignment_data)
print("Contact unassigned from group")
```

## Deleting Contacts

```python
from devhub_python.models.contacts import DeleteContactsDto

# Delete contacts
delete_data = DeleteContactsDto(contact_ids=[contact.id])
client.services.contacts.delete_bulk(delete_data)
print("Contact deleted successfully")
```

## Error Handling

```python
from devhub_python.exceptions import DevoException

try:
    contact = client.services.contacts.create(contact_data)
except DevoException as e:
    print(f"Contact creation failed: {e}")
```

!!! note "Services Namespace"
    Contacts are accessed through `client.services.contacts` to separate data management from messaging operations.
