import os
import subprocess
import sys

from devo_global_comms_python import DevoClient, DevoException


def main():
    print("🚀 Devo Global Communications SDK")
    print("=" * 60)

    # Check if API key is set
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Please set DEVO_API_KEY environment variable")
        print("   You can get your API key from the Devo dashboard")
        return

    # Initialize the client
    try:
        client = DevoClient(api_key=api_key)
        print("✅ Devo SDK Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    print("\n📋 Available Resources:")
    print("-" * 30)

    # Check available resources
    resources = []
    if hasattr(client, "sms"):
        resources.append(("📱 SMS", "Implemented", "sms_example.py"))
    if hasattr(client, "email"):
        resources.append(("📧 Email", "Placeholder", "email_example.py"))
    if hasattr(client, "whatsapp"):
        resources.append(("💬 WhatsApp", "Placeholder", "whatsapp_example.py"))
    if hasattr(client, "contacts"):
        resources.append(("👥 Contacts", "Placeholder", "contacts_example.py"))
    if hasattr(client, "contact_groups"):
        resources.append(("🗂️  Contact Groups", "Implemented", "contact_groups_example.py"))
    if hasattr(client, "rcs"):
        resources.append(("🎴 RCS", "Placeholder", "rcs_example.py"))
    if hasattr(client, "messages"):
        resources.append(("📬 Messages", "Implemented", "omni_channel_example.py"))

    for resource, status, example_file in resources:
        print(f"   {resource:<12} - {status:<12} -> {example_file}")

    # Quick SMS test if available
    if hasattr(client, "sms"):
        print("\n🧪 Quick SMS Test:")
        print("-" * 30)
        try:
            # Try to get senders as a connectivity test
            senders = client.sms.get_senders()
            print(f"✅ SMS connection successful - {len(senders.senders)} senders available")

            if senders.senders:
                print("   Sample senders:")
                for i, sender in enumerate(senders.senders[:3], 1):
                    print(f"     {i}. {sender.phone_number} ({sender.type})")
                if len(senders.senders) > 3:
                    print(f"     ... and {len(senders.senders) - 3} more")

        except DevoException as e:
            print(f"⚠️  SMS connection test failed: {e}")

    # Show example usage
    print("\n💡 Getting Started:")
    print("-" * 30)
    print("1. Run individual resource examples:")
    print("   python examples/sms_example.py              # Complete SMS functionality")
    print("   python examples/contact_groups_example.py   # Complete Contact Groups functionality")
    print("   python examples/omni_channel_example.py     # Complete Omni-channel messaging")
    print("   python examples/email_example.py            # Email examples (placeholder)")
    print("   python examples/whatsapp_example.py         # WhatsApp examples (placeholder)")
    print("   python examples/contacts_example.py         # Contact management (placeholder)")
    print("   python examples/rcs_example.py              # RCS examples (placeholder)")
    print()
    print("2. Quick SMS example:")
    print("   from devo_global_comms_python import DevoClient")
    print("   client = DevoClient(api_key='your_api_key')")
    print("   response = client.sms.send_sms(")
    print("       recipient='+1234567890',")
    print("       message='Hello from Devo!',")
    print("       sender='your_sender_id'")
    print("   )")

    # Interactive menu
    print("\n🎯 Interactive Examples:")
    print("-" * 30)
    print("Would you like to run a specific example?")
    print("1. SMS Example (full functionality)")
    print("2. Contact Groups Example (full functionality)")
    print("3. Omni-channel Messaging Example (full functionality)")
    print("4. Email Example (placeholder)")
    print("5. WhatsApp Example (placeholder)")
    print("6. Contacts Example (placeholder)")
    print("7. RCS Example (placeholder)")
    print("0. Exit")

    try:
        choice = input("\nEnter your choice (0-7): ").strip()
        example_files = {
            "1": "sms_example.py",
            "2": "contact_groups_example.py",
            "3": "omni_channel_example.py",
            "4": "email_example.py",
            "5": "whatsapp_example.py",
            "6": "contacts_example.py",
            "7": "rcs_example.py",
        }

        if choice in example_files:
            example_file = example_files[choice]
            example_path = os.path.join(os.path.dirname(__file__), example_file)

            if os.path.exists(example_path):
                print(f"\n🚀 Running {example_file}...")
                print("=" * 60)
                subprocess.run([sys.executable, example_path], check=True)
            else:
                print(f"❌ Example file {example_file} not found")
        elif choice == "0":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running example: {e}")


if __name__ == "__main__":
    main()
