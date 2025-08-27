import os

from devo_global_comms_python import DevoClient, DevoException


def main():
    # Initialize the client with your API key
    # You can get your API key from the Devo dashboard
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("Please set DEVO_API_KEY environment variable")
        return

    client = DevoClient(api_key=api_key)

    try:
        # Example 1: Send an SMS
        print("Sending SMS...")
        sms = client.sms.send(
            to="+1234567890",  # Replace with actual phone number
            body="Hello from Devo SDK! This is a test SMS message.",
        )
        print(f"SMS sent successfully! Message SID: {sms.sid}")
        print(f"Status: {sms.status}")

        # Example 2: Send an email
        print("\nSending email...")
        email = client.email.send(
            to="recipient@example.com",  # Replace with actual email
            subject="Test Email from Devo SDK",
            body="This is a test email sent using the Devo Global Communications SDK.",
            html_body="<h1>Test Email</h1><p>This is a <strong>test email</strong> sent using the Devo SDK.</p>",
        )
        print(f"Email sent successfully! Message ID: {email.id}")
        print(f"Status: {email.status}")

        # Example 3: Send a WhatsApp message
        print("\nSending WhatsApp message...")
        whatsapp = client.whatsapp.send_text(
            to="+1234567890",  # Replace with actual WhatsApp number
            text="Hello from Devo SDK! This is a WhatsApp message.",
        )
        print(f"WhatsApp message sent successfully! Message ID: {whatsapp.id}")
        print(f"Status: {whatsapp.status}")

        # Example 4: Create a contact
        print("\nCreating contact...")
        contact = client.contacts.create(
            phone_number="+1234567890",
            email="contact@example.com",
            first_name="John",
            last_name="Doe",
            company="Example Corp",
            metadata={"source": "sdk_example"},
        )
        print(f"Contact created successfully! Contact ID: {contact.id}")
        print(f"Name: {contact.first_name} {contact.last_name}")

        # Example 5: List recent messages
        print("\nListing recent messages...")
        messages = client.messages.list(limit=5, date_sent_after="2024-01-01")
        print(f"Found {len(messages)} recent messages:")
        for message in messages:
            print(f"  - {message.channel}: {message.id} ({message.status})")

    except DevoException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
