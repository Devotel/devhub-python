import os

from devo_global_comms_python import DevoClient, DevoException


def main():
    # Initialize the client with your API key
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Please set DEVO_API_KEY environment variable")
        print("   You can get your API key from the Devo dashboard")
        return

    client = DevoClient(api_key=api_key)
    print("✅ Devo SMS Client initialized successfully")
    print("=" * 60)

    try:
        # Example 1: Send SMS using new quick-send API
        print("📱 SMS QUICK-SEND API EXAMPLE")
        print("-" * 30)

        recipient = "+1234567890"  # Replace with actual phone number
        sender = "+0987654321"  # Replace with your sender number/ID
        message = "Hello from Devo SDK! This message was sent using the new quick-send API."

        print(f"📤 Sending SMS to {recipient}...")
        print(f"📝 Message: {message}")
        print(f"📞 From: {sender}")

        sms_response = client.sms.send_sms(
            recipient=recipient,
            message=message,
            sender=sender,
            hirvalidation=True,  # Enable high-quality routing validation
        )

        print("✅ SMS sent successfully!")
        print(f"   📋 Message ID: {sms_response.id}")
        print(f"   📊 Status: {sms_response.status}")
        print(f"   📱 Recipient: {sms_response.recipient}")
        print(f"   🔄 Direction: {sms_response.direction}")
        print(f"   🔧 API Mode: {sms_response.apimode}")
        if sms_response.send_date:
            print(f"   📅 Send Date: {sms_response.send_date}")

    except DevoException as e:
        print(f"❌ Failed to send SMS: {e}")
        print_error_details(e)

    print("\n" + "=" * 60)

    try:
        # Example 2: Get available senders
        print("👥 GET AVAILABLE SENDERS EXAMPLE")
        print("-" * 30)

        print("🔍 Retrieving available senders...")
        senders = client.sms.get_senders()

        print(f"✅ Found {len(senders.senders)} available senders:")
        for i, sender in enumerate(senders.senders, 1):
            print(f"   {i}. 📞 Phone: {sender.phone_number}")
            print(f"      🏷️  Type: {sender.type}")
            print(f"      🧪 Test Mode: {'Yes' if sender.istest else 'No'}")
            print(f"      🆔 ID: {sender.id}")
            if sender.creation_date:
                print(f"      📅 Created: {sender.creation_date}")
            print()

    except DevoException as e:
        print(f"❌ Failed to get senders: {e}")
        print_error_details(e)

    print("=" * 60)

    try:
        # Example 3: Get available numbers for purchase
        print("🔢 GET AVAILABLE NUMBERS EXAMPLE")
        print("-" * 30)

        region = "US"
        number_type = "mobile"
        limit = 5

        print(f"🔍 Searching for {limit} available {number_type} numbers in {region}...")
        numbers = client.sms.get_available_numbers(region=region, limit=limit, type=number_type)

        print(f"✅ Found {len(numbers.numbers)} available numbers:")
        for i, number_info in enumerate(numbers.numbers, 1):
            print(f"\n   📋 Number Group {i}:")
            for j, feature in enumerate(number_info.features, 1):
                print(f"      {j}. 📞 Number: {feature.phone_number}")
                print(f"         🏷️  Type: {feature.number_type}")
                print(f"         🌍 Region: {feature.region_information.region_name}")
                print(f"         🌐 Country: {feature.region_information.country_code}")
                print(
                    f"         💰 Monthly: {feature.cost_information.monthly_cost} {feature.cost_information.currency}"
                )
                print(f"         🔧 Setup: {feature.cost_information.setup_cost} {feature.cost_information.currency}")
                print()

    except DevoException as e:
        print(f"❌ Failed to get available numbers: {e}")
        print_error_details(e)

    print("=" * 60)

    # Example 4: Purchase a number (commented out to prevent accidental charges)
    print("💳 NUMBER PURCHASE EXAMPLE (DISABLED)")
    print("-" * 30)
    print("⚠️  The following example is commented out to prevent accidental charges.")
    print("   Uncomment and modify the code below to actually purchase a number:")
    print()
    print("   ```python")
    print("   # Choose a number from the available numbers above")
    print("   selected_number = '+1234567890'  # Replace with actual available number")
    print("   ")
    print("   print(f'💳 Purchasing number {selected_number}...')")
    print("   number_purchase = client.sms.buy_number(")
    print("       region='US',")
    print("       number=selected_number,")
    print("       number_type='mobile',")
    print("       agency_authorized_representative='Jane Doe',")
    print("       agency_representative_email='jane.doe@company.com',")
    print("       is_longcode=True,")
    print("       is_automated_enabled=True")
    print("   )")
    print("   ")
    print("   print('✅ Number purchased successfully!')")
    print("   print(f'   📞 Number: {number_purchase.number}')")
    print("   print(f'   🏷️  Type: {number_purchase.number_type}')")
    print("   print(f'   🌍 Region: {number_purchase.region}')")
    print("   print(f'   ✨ Features: {len(number_purchase.features)}')")
    print("   for feature in number_purchase.features:")
    print("       print(f'      - {feature.phone_number} ({feature.number_type})')")
    print("   ```")

    print("\n" + "=" * 60)

    try:
        # Example 5: Using legacy send method for backward compatibility
        print("🔄 LEGACY COMPATIBILITY EXAMPLE")
        print("-" * 30)

        print("🔄 Testing legacy send method for backward compatibility...")
        print("   (This uses the old API structure but maps to new implementation)")

        try:
            legacy_response = client.sms.send(
                to=recipient,
                body="Hello from legacy method! This ensures backward compatibility.",
                from_=sender,
            )
            print("✅ Legacy send successful!")
            print(f"   📋 Message ID: {legacy_response.id}")
            print(f"   📊 Status: {legacy_response.status}")

        except DevoException as e:
            print(f"⚠️  Legacy send failed (this is expected if sender is not configured): {e}")
            print("   💡 Use the new send_sms() method for better control and error handling")

    except DevoException as e:
        print(f"❌ Legacy compatibility test failed: {e}")
        print_error_details(e)

    print("\n" + "=" * 60)
    print("📊 SMS EXAMPLE SUMMARY")
    print("-" * 30)
    print("✅ Covered SMS API endpoints:")
    print("   1. 📤 POST /user-api/sms/quick-send - Send SMS messages")
    print("   2. 👥 GET /user-api/me/senders - Get available senders")
    print("   3. 🔢 GET /user-api/numbers - Get available numbers")
    print("   4. 💳 POST /user-api/numbers/buy - Purchase numbers (example only)")
    print()
    print("💡 Next steps:")
    print("   - Replace phone numbers with actual values")
    print("   - Set up proper senders in your Devo dashboard")
    print("   - Uncomment purchase example when ready to buy numbers")
    print("   - Check other example files for Email, WhatsApp, etc.")


def print_error_details(error: DevoException):
    print(f"   🔍 Error Type: {type(error).__name__}")
    if hasattr(error, "status_code") and error.status_code:
        print(f"   📊 Status Code: {error.status_code}")
    if hasattr(error, "error_code") and error.error_code:
        print(f"   🔢 Error Code: {error.error_code}")
    if hasattr(error, "response_data") and error.response_data:
        print(f"   📋 Response Data: {error.response_data}")


if __name__ == "__main__":
    main()
