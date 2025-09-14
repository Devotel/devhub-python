import os
from datetime import datetime

from devhub_python import DevoClient
from devhub_python.models.messages import SendMessageDto


def main():
    """
    Demonstrate omni-channel messaging capabilities.

    Shows how to send messages through different channels using
    the unified messages.send() endpoint with channel-specific payloads.
    """

    # Initialize the client
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("Error: DEVO_API_KEY environment variable not set")
        return

    client = DevoClient(api_key=api_key)

    print("DevHub - Omni-channel Messaging Example")
    print("=" * 70)

    # Example 1: Send SMS Message
    print("\nSending SMS Message...")
    try:
        sms_message = SendMessageDto(
            channel="sms",
            to="+1234567890",
            **{"from": "+0987654321"},  # Use dict unpacking for 'from' field
            payload={"text": "Hello from Devo! This is an SMS message."},
            callback_url="https://example.com/sms-webhook",
            metadata={"campaign": "omni-demo", "type": "sms"},
        )

        sms_result = client.messages.send(sms_message)
        print("SMS sent successfully!")
        print(f"   Message ID: {sms_result.id}")
        print(f"   Status: {sms_result.status}")
        print(f"   Channel: {sms_result.channel}")
        print(f"   Created: {sms_result.created_at}")

    except Exception as e:
        print(f"SMS Error: {str(e)}")

    # Example 2: Send Email Message
    print("\nSending Email Message...")
    try:
        email_message = SendMessageDto(
            channel="email",
            to="recipient@example.com",
            **{"from": "sender@yourcompany.com"},  # Use dict unpacking for 'from' field
            payload={
                "subject": "Welcome to DevHub!",
                "text": "Hello! This is a plain text email sent via our omni-channel API.",
                "html": """
                <html>
                <body>
                    <h2>Welcome to DevHub!</h2>
                    <p>This is an <strong>HTML email</strong> sent via our omni-channel API.</p>
                    <p>Key features:</p>
                    <ul>
                        <li>Unified API for all channels</li>
                        <li>Channel-specific payloads</li>
                        <li>Real-time status tracking</li>
                    </ul>
                    <p>Best regards,<br>The Devo Team</p>
                </body>
                </html>
                """,
                "attachments": [
                    {
                        "filename": "welcome.pdf",
                        "content_type": "application/pdf",
                        "url": "https://example.com/files/welcome.pdf",
                    }
                ],
            },
            callback_url="https://example.com/email-webhook",
            metadata={"campaign": "omni-demo", "type": "email"},
        )

        email_result = client.messages.send(email_message)
        print("Email sent successfully!")
        print(f"   Message ID: {email_result.id}")
        print(f"   Status: {email_result.status}")
        print(f"   Channel: {email_result.channel}")
        print(f"   Subject: {email_result.content.get('subject', 'N/A')}")

    except Exception as e:
        print(f"Email Error: {str(e)}")

    # Example 3: Send WhatsApp Message
    print("\nSending WhatsApp Message...")
    try:
        whatsapp_message = SendMessageDto(
            channel="whatsapp",
            to="+1234567890",
            payload={
                "type": "text",
                "text": {
                    "body": (
                        "Hello from Devo! This WhatsApp message was sent "
                        "using our omni-channel API. Pretty cool, right?"
                    )
                },
            },
            callback_url="https://example.com/whatsapp-webhook",
            metadata={"campaign": "omni-demo", "type": "whatsapp"},
        )

        whatsapp_result = client.messages.send(whatsapp_message)
        print("WhatsApp message sent successfully!")
        print(f"   Message ID: {whatsapp_result.id}")
        print(f"   Status: {whatsapp_result.status}")
        print(f"   Channel: {whatsapp_result.channel}")

    except Exception as e:
        print(f"WhatsApp Error: {str(e)}")

    # Example 4: Send WhatsApp Template Message
    print("\nSending WhatsApp Template Message...")
    try:
        whatsapp_template = SendMessageDto(
            channel="whatsapp",
            to="+1234567890",
            payload={
                "type": "template",
                "template": {
                    "name": "welcome_message",
                    "language": {"code": "en"},
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": "John Doe"},
                                {
                                    "type": "text",
                                    "text": "Devo Communications",
                                },
                            ],
                        }
                    ],
                },
            },
            metadata={"campaign": "omni-demo", "type": "whatsapp-template"},
        )

        template_result = client.messages.send(whatsapp_template)
        print("WhatsApp template sent successfully!")
        print(f"   Message ID: {template_result.id}")
        print(f"   Status: {template_result.status}")

    except Exception as e:
        print(f"WhatsApp Template Error: {str(e)}")

    # Example 5: Send RCS Message
    print("\nSending RCS Message...")
    try:
        rcs_message = SendMessageDto(
            channel="rcs",
            to="+1234567890",
            payload={
                "message_type": "text",
                "text": (
                    "Hello from Devo! This is a Rich Communication Services " "(RCS) message with enhanced features."
                ),
                "agent_id": "your-rcs-agent-id",
                "suggestions": [
                    {
                        "reply": {
                            "text": "Learn More",
                            "postback_data": "learn_more",
                        }
                    },
                    {
                        "action": {
                            "text": "Visit Website",
                            "postback_data": "visit_website",
                            "open_url": {"url": "https://devo.com"},
                        }
                    },
                ],
            },
            callback_url="https://example.com/rcs-webhook",
            metadata={"campaign": "omni-demo", "type": "rcs"},
        )

        rcs_result = client.messages.send(rcs_message)
        print("RCS message sent successfully!")
        print(f"   Message ID: {rcs_result.id}")
        print(f"   Status: {rcs_result.status}")
        print(f"   Channel: {rcs_result.channel}")

    except Exception as e:
        print(f"RCS Error: {str(e)}")

    # Example 6: Send RCS Rich Card
    print("\nSending RCS Rich Card...")
    try:
        rcs_rich_card = SendMessageDto(
            channel="rcs",
            to="+1234567890",
            payload={
                "message_type": "rich_card",
                "rich_card": {
                    "standalone_card": {
                        "card_content": {
                            "title": "DevHub",
                            "description": "Experience the power of omni-channel messaging with our unified API.",
                            "media": {
                                "height": "TALL",
                                "content_info": {
                                    "file_url": "https://example.com/images/devo-card.jpg",
                                    "force_refresh": False,
                                },
                            },
                        },
                        "card_actions": [
                            {
                                "action_type": "open_url",
                                "action_data": "https://devo.com",
                                "label": "Learn More",
                            },
                            {
                                "action_type": "dial",
                                "action_data": "+1234567890",
                                "label": "Call Us",
                            },
                        ],
                    }
                },
            },
            metadata={"campaign": "omni-demo", "type": "rcs-rich-card"},
        )

        rich_card_result = client.messages.send(rcs_rich_card)
        print("RCS rich card sent successfully!")
        print(f"   Message ID: {rich_card_result.id}")
        print(f"   Status: {rich_card_result.status}")

    except Exception as e:
        print(f"RCS Rich Card Error: {str(e)}")

    # Example 7: Bulk messaging across channels
    print("\nBulk Messaging Demo...")
    try:
        recipients = [
            {
                "channel": "sms",
                "to": "+1234567890",
                "message": "SMS bulk message",
            },
            {
                "channel": "email",
                "to": "user1@example.com",
                "message": "Email bulk message",
            },
            {
                "channel": "whatsapp",
                "to": "+1234567891",
                "message": "WhatsApp bulk message",
            },
        ]

        bulk_results = []

        for recipient in recipients:
            if recipient["channel"] == "sms":
                payload = {"text": recipient["message"]}
            elif recipient["channel"] == "email":
                payload = {
                    "subject": "Bulk Message from Devo",
                    "text": recipient["message"],
                    "html": f"<p>{recipient['message']}</p>",
                }
            elif recipient["channel"] == "whatsapp":
                payload = {
                    "type": "text",
                    "text": {"body": recipient["message"]},
                }

            bulk_message = SendMessageDto(
                channel=recipient["channel"],
                to=recipient["to"],
                payload=payload,
                metadata={"campaign": "bulk-demo", "batch_id": "batch_001"},
            )

            result = client.messages.send(bulk_message)
            bulk_results.append(result)
            print(f"   {recipient['channel'].upper()}: {result.id} -> {result.status}")

        print(f"Bulk messaging completed! Sent {len(bulk_results)} messages")

    except Exception as e:
        print(f"Bulk Messaging Error: {str(e)}")


def send_notification_example():
    """
    Example of a practical notification system using omni-channel messaging.

    This demonstrates how you might implement a notification service that
    sends the same message through different channels based on user preferences.
    """

    print("\n" + "=" * 50)
    print("Notification System Example")
    print("=" * 50)

    # Simulated user preferences
    users = [
        {
            "name": "Alice",
            "channel": "email",
            "contact": "alice@example.com",
            "language": "en",
        },
        {
            "name": "Bob",
            "channel": "sms",
            "contact": "+1234567890",
            "language": "en",
        },
        {
            "name": "Carlos",
            "channel": "whatsapp",
            "contact": "+1234567891",
            "language": "es",
        },
        {
            "name": "Diana",
            "channel": "rcs",
            "contact": "+1234567892",
            "language": "en",
        },
    ]

    # Common notification content
    notification = {
        "en": {
            "title": "System Maintenance Notice",
            "message": (
                "Our system will undergo maintenance on Sunday, 2:00 AM - 4:00 AM EST. "
                "Services may be temporarily unavailable."
            ),
        },
        "es": {
            "title": "Aviso de Mantenimiento del Sistema",
            "message": (
                "Nuestro sistema se someterá a mantenimiento el domingo de 2:00 AM a 4:00 AM EST. "
                "Los servicios pueden no estar disponibles temporalmente."
            ),
        },
    }

    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("Error: DEVO_API_KEY environment variable not set")
        return

    client = DevoClient(api_key=api_key)

    for user in users:
        try:
            content = notification[user["language"]]

            # Create channel-specific payload
            if user["channel"] == "email":
                payload = {
                    "subject": content["title"],
                    "text": content["message"],
                    "html": f"""
                    <html>
                    <body>
                        <h2>{content["title"]}</h2>
                        <p>{content["message"]}</p>
                        <p><em>This is an automated notification.</em></p>
                    </body>
                    </html>
                    """,
                }
            elif user["channel"] == "sms":
                payload = {"text": f"{content['title']}: {content['message']}"}
            elif user["channel"] == "whatsapp":
                payload = {
                    "type": "text",
                    "text": {"body": f"*{content['title']}*\n\n{content['message']}"},
                }
            elif user["channel"] == "rcs":
                payload = {
                    "message_type": "text",
                    "text": f"{content['title']}\n\n{content['message']}",
                    "suggestions": [
                        {
                            "reply": {
                                "text": "Acknowledged",
                                "postback_data": "maintenance_ack",
                            }
                        }
                    ],
                }

            # Send notification
            message = SendMessageDto(
                channel=user["channel"],
                to=user["contact"],
                payload=payload,
                metadata={
                    "notification_type": "maintenance",
                    "user_name": user["name"],
                    "language": user["language"],
                    "timestamp": datetime.now().isoformat(),
                },
            )

            result = client.messages.send(message)
            print(f"{user['name']} ({user['channel']}): {result.id} -> {result.status}")

        except Exception as e:
            print(f"Failed to notify {user['name']}: {str(e)}")

    print("\nNotification broadcast completed!")


if __name__ == "__main__":
    main()
    send_notification_example()
