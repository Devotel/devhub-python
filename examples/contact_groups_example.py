#!/usr/bin/env python3
import os
from datetime import datetime

from devo_global_comms_python import DevoClient
from devo_global_comms_python.models.contact_groups import (
    CreateContactsGroupDto,
    DeleteContactsGroupsDto,
    UpdateContactsGroupDto,
)


def main():
    """
    Demonstrate contact groups management capabilities.

    Shows how to create, read, update and delete contact groups
    using the Contact Groups API.
    """

    # Initialize the client
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Error: DEVO_API_KEY environment variable not set")
        return

    client = DevoClient(api_key=api_key)

    print("🗂️  Devo Global Communications - Contact Groups Management Example")
    print("=" * 75)

    # Example 1: List existing contact groups
    print("\n📋 Listing existing contact groups...")
    try:
        groups_list = client.contact_groups.list(page=1, limit=5)
        print(f"✅ Found {groups_list.total} total groups")
        print(f"   Page: {groups_list.page}/{groups_list.total_pages}")
        print(f"   Showing: {len(groups_list.groups)} groups")

        for i, group in enumerate(groups_list.groups, 1):
            print(f"   {i}. 📁 {group.name}")
            print(f"      ID: {group.id}")
            if group.description:
                print(f"      Description: {group.description}")
            print(f"      Contacts: {group.contacts_count or 0}")
            if group.created_at:
                print(f"      Created: {group.created_at}")

    except Exception as e:
        print(f"❌ Error listing groups: {str(e)}")

    # Example 2: Create a new contact group
    print("\n➕ Creating a new contact group...")
    try:
        new_group_data = CreateContactsGroupDto(
            name=f"API Demo Group {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description="A demonstration group created via the API",
            contact_ids=["demo_contact_1", "demo_contact_2"],
            metadata={
                "created_by": "api_example",
                "purpose": "demonstration",
                "created_at": datetime.now().isoformat(),
            },
        )

        new_group = client.contact_groups.create(new_group_data)
        print("✅ Contact group created successfully!")
        print(f"   📁 Name: {new_group.name}")
        print(f"   🆔 ID: {new_group.id}")
        print(f"   📝 Description: {new_group.description}")
        print(f"   👥 Contacts: {new_group.contacts_count or 0}")
        if new_group.created_at:
            print(f"   📅 Created: {new_group.created_at}")

        created_group_id = new_group.id

    except Exception as e:
        print(f"❌ Error creating group: {str(e)}")
        created_group_id = None

    # Example 3: Update the created group
    if created_group_id:
        print(f"\n✏️  Updating contact group {created_group_id}...")
        try:
            update_data = UpdateContactsGroupDto(
                name=f"Updated API Demo Group {datetime.now().strftime('%H%M%S')}",
                description="This group has been updated via the API",
                metadata={"updated_by": "api_example", "updated_at": datetime.now().isoformat(), "version": "2.0"},
            )

            updated_group = client.contact_groups.update(created_group_id, update_data)
            print("✅ Contact group updated successfully!")
            print(f"   📁 New name: {updated_group.name}")
            print(f"   📝 New description: {updated_group.description}")
            if updated_group.updated_at:
                print(f"   📅 Updated: {updated_group.updated_at}")

        except Exception as e:
            print(f"❌ Error updating group: {str(e)}")

    # Example 4: Get specific group by ID
    if created_group_id:
        print(f"\n🔍 Retrieving specific group {created_group_id}...")
        try:
            specific_group = client.contact_groups.get_by_id(created_group_id)
            print("✅ Group retrieved successfully!")
            print(f"   📁 Name: {specific_group.name}")
            print(f"   📝 Description: {specific_group.description}")
            print(f"   👥 Contacts: {specific_group.contacts_count or 0}")
            print(f"   👤 Owner: {specific_group.user_id}")

        except Exception as e:
            print(f"❌ Error retrieving group: {str(e)}")

    # Example 5: Search contact groups
    print("\n🔎 Searching contact groups...")
    try:
        search_results = client.contact_groups.search(query="demo", fields=["name", "description"], page=1, limit=10)
        print(f"✅ Search completed! Found {search_results.total} matching groups")

        for i, group in enumerate(search_results.groups, 1):
            print(f"   {i}. 📁 {group.name}")
            print(f"      🆔 ID: {group.id}")
            if group.description:
                print(f"      📝 Description: {group.description}")

    except Exception as e:
        print(f"❌ Error searching groups: {str(e)}")

    # Example 6: Advanced listing with filters
    print("\n🔧 Advanced group listing with filters...")
    try:
        filtered_groups = client.contact_groups.list(
            page=1, limit=3, search="demo", search_fields=["name", "description"]
        )
        print("✅ Filtered listing completed!")
        print(f"   Total groups matching 'demo': {filtered_groups.total}")
        print(f"   Showing page {filtered_groups.page} of {filtered_groups.total_pages}")

        for group in filtered_groups.groups:
            print(f"   📁 {group.name} (ID: {group.id})")

    except Exception as e:
        print(f"❌ Error with filtered listing: {str(e)}")

    # Example 7: Bulk operations demonstration
    print("\n📦 Bulk operations example...")

    # First, let's create a few more groups for bulk operations
    bulk_group_ids = []

    try:
        for i in range(3):
            bulk_group_data = CreateContactsGroupDto(
                name=f"Bulk Demo Group {i+1}",
                description=f"Group {i+1} for bulk operations demo",
                metadata={"bulk_demo": True, "group_number": i + 1},
            )

            bulk_group = client.contact_groups.create(bulk_group_data)
            bulk_group_ids.append(bulk_group.id)
            print(f"   ✅ Created bulk group {i+1}: {bulk_group.name}")

        print(f"📊 Created {len(bulk_group_ids)} groups for bulk demo")

    except Exception as e:
        print(f"❌ Error creating bulk groups: {str(e)}")

    # Example 8: Individual group deletion
    if created_group_id:
        print(f"\n🗑️  Deleting individual group {created_group_id}...")
        try:
            deleted_group = client.contact_groups.delete_by_id(created_group_id, approve="yes")
            print("✅ Individual group deleted successfully!")
            print(f"   📁 Deleted group: {deleted_group.name}")

        except Exception as e:
            print(f"❌ Error deleting individual group: {str(e)}")

    # Example 9: Bulk deletion
    if bulk_group_ids:
        print(f"\n🗑️  Performing bulk deletion of {len(bulk_group_ids)} groups...")
        try:
            # Create backup group first
            backup_group_data = CreateContactsGroupDto(
                name="Backup Group for Bulk Delete Demo", description="Temporary group to receive transferred contacts"
            )
            backup_group = client.contact_groups.create(backup_group_data)

            # Perform bulk deletion
            bulk_delete_data = DeleteContactsGroupsDto(group_ids=bulk_group_ids, transfer_contacts_to=backup_group.id)

            bulk_delete_result = client.contact_groups.delete_bulk(bulk_delete_data, approve="yes")
            print("✅ Bulk deletion completed successfully!")
            print(f"   📊 Operation result: {bulk_delete_result.name}")

            # Clean up backup group
            client.contact_groups.delete_by_id(backup_group.id, approve="yes")
            print("   🧹 Cleaned up backup group")

        except Exception as e:
            print(f"❌ Error with bulk deletion: {str(e)}")

    # Example 10: Error handling demonstration
    print("\n⚠️  Error handling demonstration...")
    try:
        # Try to get a non-existent group
        client.contact_groups.get_by_id("non_existent_group_id")

    except Exception as e:
        print(f"✅ Properly handled expected error: {type(e).__name__}")
        print(f"   Error message: {str(e)}")

    print("\n" + "=" * 75)
    print("🎯 Contact Groups management demo completed!")
    print("\nKey Features Demonstrated:")
    print("• ✅ List groups with pagination and search")
    print("• ✅ Create new contact groups with metadata")
    print("• ✅ Update existing groups")
    print("• ✅ Retrieve specific groups by ID")
    print("• ✅ Search groups with field filtering")
    print("• ✅ Individual group deletion")
    print("• ✅ Bulk group deletion with contact transfer")
    print("• ✅ Comprehensive error handling")


def contact_group_management_workflow():
    """
    Example of a complete contact group management workflow.

    Demonstrates a realistic scenario of managing contact groups
    for different business purposes.
    """

    print("\n" + "=" * 60)
    print("📊 Contact Group Management Workflow Example")
    print("=" * 60)

    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Error: DEVO_API_KEY environment variable not set")
        return

    client = DevoClient(api_key=api_key)

    # Define different types of contact groups for a business
    group_types = [
        {
            "name": "VIP Customers",
            "description": "High-value customers requiring priority support",
            "metadata": {"priority": "high", "support_tier": "premium"},
        },
        {
            "name": "Newsletter Subscribers",
            "description": "Contacts subscribed to weekly newsletter",
            "metadata": {"communication_type": "newsletter", "frequency": "weekly"},
        },
        {
            "name": "Product Beta Testers",
            "description": "Users participating in beta testing programs",
            "metadata": {"program": "beta", "access_level": "testing"},
        },
        {
            "name": "Sales Prospects",
            "description": "Potential customers in the sales pipeline",
            "metadata": {"stage": "prospect", "department": "sales"},
        },
    ]

    created_groups = []

    # Create business contact groups
    print("\n🏢 Creating business contact groups...")
    for group_type in group_types:
        try:
            group_data = CreateContactsGroupDto(
                name=group_type["name"], description=group_type["description"], metadata=group_type["metadata"]
            )

            group = client.contact_groups.create(group_data)
            created_groups.append(group)
            print(f"   ✅ Created: {group.name}")

        except Exception as e:
            print(f"   ❌ Error creating {group_type['name']}: {str(e)}")

    # Demonstrate group analytics
    print("\n📊 Group Analytics:")
    print(f"   Total groups created: {len(created_groups)}")

    for group in created_groups:
        print(f"   📁 {group.name}")
        print(f"      📈 Current contacts: {group.contacts_count or 0}")
        print(f"      🏷️  Category: {group.metadata.get('priority', 'standard')}")

    # Simulate group reorganization
    print("\n🔄 Reorganizing groups...")

    # Update VIP group to include more metadata
    vip_group = next((g for g in created_groups if "VIP" in g.name), None)
    if vip_group:
        try:
            update_data = UpdateContactsGroupDto(
                description="Premium customers with dedicated account management",
                metadata={
                    **vip_group.metadata,
                    "account_manager": "assigned",
                    "response_time": "< 1 hour",
                    "last_updated": datetime.now().isoformat(),
                },
            )

            client.contact_groups.update(vip_group.id, update_data)
            print("   ✅ Updated VIP group with enhanced metadata")

        except Exception as e:
            print(f"   ❌ Error updating VIP group: {str(e)}")

    # Clean up demonstration groups
    print("\n🧹 Cleaning up demonstration groups...")
    if created_groups:
        try:
            group_ids = [group.id for group in created_groups]

            # Create a temporary group for contact transfer
            temp_group_data = CreateContactsGroupDto(
                name="Temporary Archive", description="Temporary group for workflow cleanup"
            )
            temp_group = client.contact_groups.create(temp_group_data)

            # Bulk delete with contact transfer
            delete_data = DeleteContactsGroupsDto(group_ids=group_ids, transfer_contacts_to=temp_group.id)

            client.contact_groups.delete_bulk(delete_data, approve="yes")
            print(f"   ✅ Bulk deleted {len(group_ids)} demonstration groups")

            # Delete temporary group
            client.contact_groups.delete_by_id(temp_group.id, approve="yes")
            print("   ✅ Cleaned up temporary archive group")

        except Exception as e:
            print(f"   ❌ Error during cleanup: {str(e)}")

    print("\n🎯 Workflow demonstration completed!")


if __name__ == "__main__":
    main()
    contact_group_management_workflow()
