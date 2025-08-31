# Contact Groups

The Contact Groups resource allows you to organize contacts into groups for easier management.

## Creating Contact Groups

```python
from devo_global_comms_python.models.contact_groups import CreateContactsGroupDto

# Create a contact group
group_data = CreateContactsGroupDto(
    name="VIP Customers",
    description="High-value customers",
    contact_ids=["contact_1", "contact_2"]  # Optional initial contacts
)

group = client.services.contact_groups.create(group_data)
print(f"Contact group created with ID: {group.id}")
```

## Listing Contact Groups

```python
# List contact groups with pagination
groups_response = client.services.contact_groups.list(page=1, limit=10)
print(f"Found {groups_response.total} contact groups")

for group in groups_response.groups:
    print(f"Group: {group.name} - {group.description}")
    print(f"Contacts: {len(group.contact_ids or [])} members")
```

## Updating Contact Groups

```python
from devo_global_comms_python.models.contact_groups import UpdateContactsGroupDto

# Update a contact group
update_data = UpdateContactsGroupDto(
    name="Premium VIP Customers",
    description="Updated description for high-value customers"
)

updated_group = client.services.contact_groups.update(group.id, update_data)
print(f"Group updated: {updated_group.name}")
```

## Managing Group Membership

### Adding Contacts to Group

```python
# Add contacts to an existing group
add_data = UpdateContactsGroupDto(
    contact_ids=["new_contact_1", "new_contact_2"]
)

client.services.contact_groups.update(group.id, add_data)
print("Contacts added to group")
```

### Removing Contacts from Group

```python
# Remove specific contacts from group
remove_data = UpdateContactsGroupDto(
    contact_ids=[]  # Empty list removes all contacts
)

client.services.contact_groups.update(group.id, remove_data)
print("Contacts removed from group")
```

## Searching Contact Groups

```python
# Search contact groups by name
search_results = client.services.contact_groups.list(
    page=1,
    limit=5,
    search="VIP"
)
print(f"Found {search_results.total} groups matching 'VIP'")
```

## Deleting Contact Groups

```python
from devo_global_comms_python.models.contact_groups import DeleteContactsGroupsDto

# Delete contact groups
delete_data = DeleteContactsGroupsDto(
    group_ids=[group.id],
    transfer_contacts_to="another_group_id"  # Optional: transfer contacts before deletion
)

client.services.contact_groups.delete_bulk(delete_data)
print("Contact group deleted successfully")
```

## Error Handling

```python
from devo_global_comms_python.exceptions import DevoException

try:
    group = client.services.contact_groups.create(group_data)
except DevoException as e:
    print(f"Contact group creation failed: {e}")
```

!!! tip "Group Organization"
    Use contact groups to segment your audience for targeted messaging campaigns and better contact management.
