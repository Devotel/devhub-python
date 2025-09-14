import os

from devhub_python import DevoClient
from devhub_python.exceptions import DevoException
from devhub_python.models.contacts import (
    AssignToContactsGroupDto,
    CreateContactDto,
    CreateCustomFieldDto,
    DeleteContactsDto,
    UpdateContactDto,
    UpdateCustomFieldDto,
)


def main():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("Please set DEVO_API_KEY environment variable")
        return

    client = DevoClient(api_key=api_key)
    print("DevHub - Contacts Management Example")
    print("=" * 60)

    try:
        # Example 1: List existing contacts
        print("1. LIST CONTACTS")
        print("-" * 30)
        contacts_response = client.services.contacts.list(page=1, limit=5)
        print(f"Found {contacts_response.total} total contacts")
        print(f"Page: {contacts_response.page}/{contacts_response.total_pages}")
        print(f"Showing: {len(contacts_response.contacts)} contacts")

        for i, contact in enumerate(contacts_response.contacts, 1):
            name = f"{contact.first_name or ''} {contact.last_name or ''}".strip()
            print(f"  {i}. {name or 'Unnamed Contact'}")
            print(f"     ID: {contact.id}")
            if contact.email:
                print(f"     Email: {contact.email}")
            if contact.phone_number:
                print(f"     Phone: {contact.phone_number}")
            if contact.company:
                print(f"     Company: {contact.company}")

        # Example 2: Create a new contact
        print("\n2. CREATE CONTACT")
        print("-" * 30)
        create_data = CreateContactDto(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            company="Acme Corp",
            tags=["customer", "test"],
            metadata={"source": "sdk_example", "campaign": "Q1_2025"},
        )

        new_contact = client.services.contacts.create(create_data)
        print("Contact created successfully!")
        print(f"ID: {new_contact.id}")
        print(f"Name: {new_contact.first_name} {new_contact.last_name}")
        print(f"Email: {new_contact.email}")
        print(f"Phone: {new_contact.phone_number}")

        # Example 3: Update the contact
        print("\n3. UPDATE CONTACT")
        print("-" * 30)
        update_data = UpdateContactDto(
            company="Acme Corporation Ltd",
            tags=["customer", "vip", "updated"],
            metadata={"source": "sdk_example", "updated": "2025-08-31"},
        )

        updated_contact = client.services.contacts.update(new_contact.id, update_data)
        print("Contact updated successfully!")
        print(f"ID: {updated_contact.id}")
        print(f"Updated company: {updated_contact.company}")
        print(f"Updated tags: {updated_contact.tags}")

        # Example 4: List contacts with filtering
        print("\n4. LIST CONTACTS WITH FILTERING")
        print("-" * 30)
        filtered_contacts = client.services.contacts.list(
            page=1, limit=10, search="Acme", is_email_subscribed=True, tags=["customer"]
        )
        print(f"Found {filtered_contacts.total} contacts matching filters")
        for contact in filtered_contacts.contacts:
            name = f"{contact.first_name or ''} {contact.last_name or ''}".strip()
            print(f"  - {name or 'Unnamed'} ({contact.company or 'No Company'})")

        # Example 5: Custom fields management
        print("\n5. CUSTOM FIELDS MANAGEMENT")
        print("-" * 30)

        # List existing custom fields
        custom_fields = client.services.contacts.list_custom_fields(page=1, limit=5)
        print(f"Found {custom_fields.total} custom fields")

        # Create a new custom field
        field_data = CreateCustomFieldDto(
            name="Department", field_type="text", description="Employee department", is_required=False
        )

        new_field = client.services.contacts.create_custom_field(field_data)
        print(f"Custom field created: {new_field.name} (ID: {new_field.id})")

        # Update the custom field
        update_field_data = UpdateCustomFieldDto(description="Employee department (updated)", is_required=True)

        client.services.contacts.update_custom_field(new_field.id, update_field_data)
        print("Custom field updated successfully")

        # Example 6: Contact group assignment
        print("\n6. CONTACT GROUP ASSIGNMENT")
        print("-" * 30)

        # List contact groups first
        contact_groups = client.services.contact_groups.list(page=1, limit=5)
        if contact_groups.groups:
            first_group = contact_groups.groups[0]
            print(f"Found contact group: {first_group.name} (ID: {first_group.id})")

            # Assign contact to group
            assignment_data = AssignToContactsGroupDto(contact_ids=[new_contact.id], contacts_group_id=first_group.id)

            client.services.contacts.assign_to_group(assignment_data)
            print(f"Contact assigned to group: {first_group.name}")

            # Unassign contact from group
            client.services.contacts.unassign_from_group(assignment_data)
            print(f"Contact unassigned from group: {first_group.name}")
        else:
            print("No contact groups available for assignment demo")

        # Example 7: Delete the test contact
        print("\n7. DELETE CONTACT")
        print("-" * 30)
        delete_data = DeleteContactsDto(contact_ids=[new_contact.id])

        client.services.contacts.delete_bulk(delete_data)
        print(f"Contact deleted successfully (ID: {new_contact.id})")

    except DevoException as e:
        print(f"Contacts operation failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
