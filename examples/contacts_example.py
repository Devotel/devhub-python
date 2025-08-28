import os

from devo_global_comms_python import DevoException


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
    print("💡 To implement:")
    print("   1. Define Contacts API endpoints and specifications")
    print("   2. Create Contact Pydantic models")
    print("   3. Implement ContactsResource class")
    print("   4. Update this example with real functionality")
    print("   5. Add support for CRUD operations and contact management")


if __name__ == "__main__":
    main()
