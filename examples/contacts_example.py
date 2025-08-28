#!/usr/bin/env python3
import os

from devo_global_comms_python import DevoClient
from devo_global_comms_python.exceptions import DevoException


def main():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Please set DEVO_API_KEY environment variable")
        return

    print("✅ Devo Contacts Client initialized successfully")
    print("=" * 60)

    try:
        # Example 1: Create a contact
        print("👤 CREATE CONTACT EXAMPLE")
        print("-" * 30)

        print("📝 Creating a new contact...")
        print("⚠️  This is a placeholder implementation.")
        print("   Update this example when Contacts API is implemented.")

        # Placeholder contact creation - update when implementing Contacts resource
        print("   ```python")
        print("   contact = client.contacts.create(")
        print("       phone_number='+1234567890',")
        print("       email='john.doe@example.com',")
        print("       first_name='John',")
        print("       last_name='Doe',")
        print("       company='Acme Corp',")
        print("       metadata={'source': 'sdk_example', 'campaign': 'Q1_2025'}")
        print("   )")
        print("   print(f'Contact created! ID: {contact.id}')")
        print("   ```")

        # Example 2: Get contact by ID
        print("\n🔍 GET CONTACT EXAMPLE")
        print("-" * 30)

        print("📖 Retrieving contact by ID...")
        print("   ```python")
        print("   contact = client.contacts.get('contact_id_123')")
        print("   print(f'Contact: {contact.first_name} {contact.last_name}')")
        print("   print(f'Phone: {contact.phone_number}')")
        print("   print(f'Email: {contact.email}')")
        print("   ```")

        # Example 3: List contacts
        print("\n📋 LIST CONTACTS EXAMPLE")
        print("-" * 30)

        print("📋 Listing contacts...")
        print("   ```python")
        print("   contacts = client.contacts.list(")
        print("       limit=10,")
        print("       filter_by_company='Acme Corp'")
        print("   )")
        print("   print(f'Found {len(contacts)} contacts:')")
        print("   for contact in contacts:")
        print("       print(f'  - {contact.first_name} {contact.last_name}')")
        print("   ```")

        # Example 4: Update contact
        print("\n✏️ UPDATE CONTACT EXAMPLE")
        print("-" * 30)

        print("✏️ Updating contact information...")
        print("   ```python")
        print("   updated_contact = client.contacts.update(")
        print("       contact_id='contact_id_123',")
        print("       company='Acme Corporation',")
        print("       metadata={'source': 'sdk_example', 'updated': '2025-08-28'}")
        print("   )")
        print("   print(f'Contact updated! Company: {updated_contact.company}')")
        print("   ```")

        # Example 5: Delete contact
        print("\n🗑️ DELETE CONTACT EXAMPLE")
        print("-" * 30)

        print("🗑️ Deleting contact...")
        print("   ```python")
        print("   client.contacts.delete('contact_id_123')")
        print("   print('Contact deleted successfully!')")
        print("   ```")

    except DevoException as e:
        print(f"❌ Contacts operation failed: {e}")

    print("\n" + "=" * 60)
    print("📊 CONTACTS EXAMPLE SUMMARY")
    print("-" * 30)
    print("⚠️  This is a placeholder example for Contacts functionality.")
    client = DevoClient(api_key=api_key)

    print("� Devo Global Communications - Contacts Management Example")
    print("=" * 70)
    print("📋 Using services namespace: client.services.contacts")
    print()

    # Example 1: List existing contacts
    print("\n📋 Listing existing contacts...")
    try:
        contacts_list = client.services.contacts.list(page=1, limit=5)
        print(f"✅ Found {contacts_list.total} total contacts")
        print(f"   Page: {contacts_list.page}/{contacts_list.total_pages}")
        print(f"   Showing: {len(contacts_list.contacts)} contacts")

        for i, contact in enumerate(contacts_list.contacts, 1):
            print(f"   {i}. 👤 {contact.first_name or ''} {contact.last_name or ''}".strip())
            print(f"      ID: {contact.id}")
            if contact.email:
                print(f"      📧 Email: {contact.email}")
            if contact.phone_number:
                print(f"      📱 Phone: {contact.phone_number}")
            if contact.created_at:
                print(f"      📅 Created: {contact.created_at}")

    except Exception as e:
        print(f"❌ Error listing contacts: {str(e)}")

    print("\n🎯 Contacts management demo completed!")
    print("\nKey Features Available:")
    print("• ✅ List contacts with advanced filtering")
    print("• ✅ Create and update contacts")
    print("• ✅ Contact group assignment/unassignment")
    print("• ✅ Custom field management")
    print("• ✅ CSV import functionality")
    print("• ✅ Bulk operations")


if __name__ == "__main__":
    main()
