import os

from devo_global_comms_python import DevoException


def main():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Please set DEVO_API_KEY environment variable")
        return

    print("✅ Devo WhatsApp Client initialized successfully")
    print("=" * 60)

    try:
        # Example 1: Send a text message
        print("💬 WHATSAPP TEXT MESSAGE EXAMPLE")
        print("-" * 30)

        print("📤 Sending WhatsApp text message...")
        print("⚠️  This is a placeholder implementation.")
        print("   Update this example when WhatsApp API is implemented.")

        # Placeholder WhatsApp send - update when implementing WhatsApp resource
        print("   ```python")
        print("   whatsapp_response = client.whatsapp.send_text(")
        print("       to='+1234567890',")
        print("       text='Hello from Devo SDK via WhatsApp!'")
        print("   )")
        print("   print(f'WhatsApp message sent! ID: {whatsapp_response.id}')")
        print("   ```")

        # Example 2: Send media message
        print("\n📷 WHATSAPP MEDIA MESSAGE EXAMPLE")
        print("-" * 30)

        print("📤 Sending WhatsApp media message...")
        print("   ```python")
        print("   media_response = client.whatsapp.send_media(")
        print("       to='+1234567890',")
        print("       media_url='https://example.com/image.jpg',")
        print("       media_type='image',")
        print("       caption='Check out this image!'")
        print("   )")
        print("   print(f'WhatsApp media sent! ID: {media_response.id}')")
        print("   ```")

        # Example 3: Send template message
        print("\n📋 WHATSAPP TEMPLATE MESSAGE EXAMPLE")
        print("-" * 30)

        print("📤 Sending WhatsApp template message...")
        print("   ```python")
        print("   template_response = client.whatsapp.send_template(")
        print("       to='+1234567890',")
        print("       template_name='welcome_message',")
        print("       template_variables={'name': 'John', 'company': 'Acme Corp'}")
        print("   )")
        print("   print(f'WhatsApp template sent! ID: {template_response.id}')")
        print("   ```")

    except DevoException as e:
        print(f"❌ WhatsApp operation failed: {e}")

    print("\n" + "=" * 60)
    print("📊 WHATSAPP EXAMPLE SUMMARY")
    print("-" * 30)
    print("⚠️  This is a placeholder example for WhatsApp functionality.")
    print("💡 To implement:")
    print("   1. Define WhatsApp API endpoints and specifications")
    print("   2. Create WhatsApp Pydantic models")
    print("   3. Implement WhatsAppResource class")
    print("   4. Update this example with real functionality")
    print("   5. Add support for text, media, and template messages")


if __name__ == "__main__":
    main()
