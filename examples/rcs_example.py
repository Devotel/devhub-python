import os

from devhub_python import DevoClient, DevoException
from devhub_python.models.rcs import RcsSendMessageSerializer


def main():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("Please set DEVO_API_KEY environment variable")
        return

    client = DevoClient(api_key=api_key)
    print("Devo RCS Client initialized successfully")
    print("=" * 60)

    try:
        # Example 1: Get RCS accounts
        print("RCS ACCOUNTS EXAMPLE")
        print("-" * 30)

        print("Retrieving RCS accounts...")
        accounts = client.rcs.get_accounts(page=1, limit=5)

        print(f"Found {len(accounts)} RCS accounts")
        for i, account in enumerate(accounts, 1):
            print(f"   {i}. Account: {account.name}")
            print(f"      ID: {account.id}")
            print(f"      Brand: {account.brand_name}")
            print(f"      Email: {account.contact_email}")
            print(f"      Phone: {account.contact_phone}")
            print(f"      Approved: {account.is_approved}")
            print(f"      Created: {account.created_at}")

    except DevoException as e:
        print(f"Error retrieving RCS accounts: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        # Example 2: Send RCS text message using legacy method
        print("\nRCS TEXT MESSAGE EXAMPLE (Legacy)")
        print("-" * 40)

        print("Sending RCS text message...")
        text_response = client.rcs.send_text(
            to="+1234567890",  # Replace with recipient phone number
            text="Hello from Devo RCS SDK! This is a test message.",
            callback_url="https://example.com/webhook",
            metadata={"campaign": "test", "source": "sdk_example"},
        )

        print("RCS text message sent successfully!")
        print(f"   Message ID: {text_response.id}")
        print(f"   Status: {text_response.status}")
        print(f"   To: {text_response.to}")
        print(f"   Direction: {text_response.direction}")
        print(f"   Type: {text_response.type}")
        if text_response.date_created:
            print(f"   Created: {text_response.date_created}")
        if text_response.date_sent:
            print(f"   Sent: {text_response.date_sent}")

    except DevoException as e:
        print(f"Error sending RCS text: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        # Example 3: Send RCS rich card using legacy method
        print("\nRCS RICH CARD EXAMPLE (Legacy)")
        print("-" * 40)

        print("Sending RCS rich card...")
        rich_card_response = client.rcs.send_rich_card(
            to="+1234567890",  # Replace with recipient phone number
            title="Welcome to Devo",
            description="Experience our premium communication services",
            media_url="https://example.com/image.jpg",  # Replace with actual image URL
            actions=[
                {"type": "openUrl", "text": "Learn More", "url": "https://example.com/learn-more"},
                {"type": "dial", "text": "Call Us", "phoneNumber": "+1234567890"},
            ],
            callback_url="https://example.com/webhook",
            metadata={"campaign": "rich_card_demo"},
        )

        print("RCS rich card sent successfully!")
        print(f"   Message ID: {rich_card_response.id}")
        print(f"   Status: {rich_card_response.status}")
        print(f"   Type: {rich_card_response.type}")
        if rich_card_response.rich_card:
            print(f"   Card Title: {rich_card_response.rich_card.get('title', 'N/A')}")

    except DevoException as e:
        print(f"Error sending RCS rich card: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        # Example 4: Send message using the general send_message method
        print("\nRCS MESSAGE (General API)")
        print("-" * 30)

        print("Sending RCS message via general API...")

        message_data = {
            "to": "+1234567890",
            "from": "+0987654321",
            "account_id": "your_account_id",  # Replace with actual account ID
            "message_type": "text",
            "text": "Hello from the general RCS API!",
            "callback_url": "https://example.com/webhook",
            "metadata": {"source": "general_api_example"},
        }

        send_response: RcsSendMessageSerializer = client.rcs.send_message(message_data)

        print("Message sent via general API!")
        print(f"   Message ID: {send_response.id}")
        print(f"   Account ID: {send_response.account_id}")
        print(f"   Status: {send_response.status}")
        print(f"   Message Type: {send_response.message_type}")
        print(f"   Created: {send_response.created_at}")
        if send_response.sent_at:
            print(f"   Sent: {send_response.sent_at}")

    except DevoException as e:
        print(f"Error with general RCS API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        # Example 5: List RCS messages
        print("\nRCS MESSAGES LIST EXAMPLE")
        print("-" * 30)

        print("Retrieving RCS messages...")
        messages = client.rcs.list_messages(page=1, limit=5, type="text")

        print(f"Found {len(messages)} RCS messages")
        for i, message in enumerate(messages, 1):
            print(f"   {i}. Message ID: {message.id}")
            print(f"      Type: {message.message_type}")
            print(f"      Status: {message.status}")
            print(f"      To: {message.to}")
            print(f"      Created: {message.created_at}")

    except DevoException as e:
        print(f"Error listing RCS messages: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
