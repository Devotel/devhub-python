import os

from devo_global_comms_python import DevoClient, DevoException


def main():
    # Initialize the client with your API key
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("Please set DEVO_API_KEY environment variable")
        print("You can get your API key from the Devo dashboard")
        return

    client = DevoClient(api_key=api_key)
    print("Devo SMS Client initialized successfully")
    print("=" * 60)

    try:
        # Example 1: Send SMS using new quick-send API
        print("SMS QUICK-SEND API EXAMPLE")
        print("-" * 30)

        recipient = "+1234567890"  # Replace with actual phone number
        sender = "+0987654321"  # Replace with your sender number/ID
        message = "Hello from Devo SDK! This message was sent using the new quick-send API."

        print(f"Sending SMS to {recipient}...")
        print(f"Message: {message}")
        print(f"From: {sender}")

        sms_response = client.sms.send_sms(
            recipient=recipient,
            message=message,
            sender=sender,
            hirvalidation=True,  # Enable high-quality routing validation
        )

        print("SMS sent successfully!")
        print(f"   Message ID: {sms_response.id}")
        print(f"   Status: {sms_response.status}")
        print(f"   Recipient: {sms_response.recipient}")
        print(f"   Direction: {sms_response.direction}")
        print(f"   API Mode: {sms_response.apimode}")
        if sms_response.sent_date:
            print(f"   Sent Date: {sms_response.sent_date}")

    except DevoException as e:
        print(f"Failed to send SMS: {e}")

    print("\n" + "=" * 60)

    try:
        # Example 2: Get available senders
        print("GET AVAILABLE SENDERS EXAMPLE")
        print("-" * 30)

        print("Retrieving available senders...")
        senders = client.sms.get_senders()

        print(f"Found {len(senders.senders)} available senders:")
        for i, sender in enumerate(senders.senders, 1):
            print(f"   {i}. Phone: {sender.phone_number}")
            print(f"      Type: {sender.type}")
            print(f"      Test Mode: {'Yes' if sender.istest else 'No'}")
            print(f"      ID: {sender.id}")
            if sender.creation_date:
                print(f"      Created: {sender.creation_date}")
            print()

    except DevoException as e:
        print(f"Failed to get senders: {e}")

    print("=" * 60)

    try:
        # Example 3: Get available numbers for purchase
        print("GET AVAILABLE NUMBERS EXAMPLE")
        print("-" * 30)

        region = "US"
        number_type = "mobile"
        limit = 5

        print(f"Searching for {limit} available {number_type} numbers in {region}...")
        numbers = client.sms.get_available_numbers(region=region, limit=limit, type=number_type)

        print(f"Found {len(numbers.numbers)} available numbers:")
        for i, number_info in enumerate(numbers.numbers, 1):
            print(f"\n   Number Group {i}:")
            if number_info.features:
                for j, feature in enumerate(number_info.features, 1):
                    print(f"      {j}. Number: {feature.phone_number}")
                    print(f"         Type: {feature.number_type}")
                    print(f"         Region Info: {feature.region_information}")
                    print(f"         Cost Info: {feature.cost_information}")
                    print(f"         Best Effort: {feature.best_effort}")
                    print(f"         Quickship: {feature.quickship}")
                    print()
            else:
                print(f"      Phone: {number_info.phone_number}")
                print(f"      Type: {number_info.phone_number_type}")
                print(f"      Region Info: {number_info.region_information}")
                print(f"      Cost Info: {number_info.cost_information}")
                print(f"      Carrier: {number_info.carrier}")
                print()

    except DevoException as e:
        print(f"Failed to get available numbers: {e}")


if __name__ == "__main__":
    main()
