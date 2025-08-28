import os

from devo_global_comms_python import DevoCommsClient, DevoException


def main():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Please set DEVO_API_KEY environment variable")
        return

    client = DevoCommsClient(api_key=api_key)
    print("✅ Devo Email Client initialized successfully")
    print("=" * 60)

    try:
        # Example: Send an email using the Email API
        print("📧 EMAIL SEND EXAMPLE")
        print("-" * 30)

        print("📤 Sending email...")
        email_response = client.email.send_email(
            subject="Test Email from Devo SDK",
            body="This is a test email sent using the Devo Global Communications Python SDK.",
            sender="sender@example.com",
            recipient="recipient@example.com",
        )

        print("✅ Email sent successfully!")
        print(f"   📧 Message ID: {email_response.message_id}")
        print(f"   📦 Bulk Email ID: {email_response.bulk_email_id}")
        print(f"   📝 Subject: {email_response.subject}")
        print(f"   📊 Status: {email_response.status}")
        print(f"   💬 Message: {email_response.message}")
        print(f"   🕐 Timestamp: {email_response.timestamp}")
        print(f"   ✅ Success: {email_response.success}")

        # Example with different content
        print("\n📧 SENDING EMAIL WITH RICH CONTENT")
        print("-" * 40)

        rich_email_response = client.email.send_email(
            subject="🎉 Welcome to Devo Communications!",
            body=(
                "Dear valued customer,\n\n"
                "Welcome to our service! We're excited to have you on board.\n\n"
                "Best regards,\nThe Devo Team"
            ),
            sender="welcome@yourcompany.com",
            recipient="newcustomer@example.com",
        )

        print("✅ Rich content email sent!")
        print(f"   📧 Message ID: {rich_email_response.message_id}")
        print(f"   📊 Status: {rich_email_response.status}")
        print(f"   ✅ Success: {rich_email_response.success}")

    except DevoException as e:
        print(f"❌ Email operation failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print("\n" + "=" * 60)
    print("📊 EMAIL EXAMPLE SUMMARY")
    print("-" * 30)
    print("✅ Email API implementation complete!")
    print("📤 Successfully demonstrated:")
    print("   • Basic email sending")
    print("   • Email with rich content and emojis")
    print("   • Response parsing and status checking")
    print("   • Error handling")
    print("\n💡 Features available:")
    print("   • Subject and body content")
    print("   • Sender and recipient validation")
    print("   • Message tracking with unique IDs")
    print("   • Status monitoring")
    print("   • Timestamp tracking")


if __name__ == "__main__":
    main()
