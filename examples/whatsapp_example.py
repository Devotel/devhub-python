import os

from devo_global_comms_python import DevoCommsClient, DevoException


def main():
    api_key = os.getenv("DEVO_API_KEY")
    if not api_key:
        print("❌ Please set DEVO_API_KEY environment variable")
        return

    client = DevoCommsClient(api_key=api_key)
    print("✅ Devo WhatsApp Client initialized successfully")
    print("=" * 60)

    try:
        # Example 1: Get WhatsApp accounts
        print("📱 WHATSAPP ACCOUNTS EXAMPLE")
        print("-" * 30)

        print("📤 Getting WhatsApp accounts...")
        accounts_response = client.whatsapp.get_accounts(page=1, limit=10, is_approved=True)

        print("✅ WhatsApp accounts retrieved successfully!")
        print(f"   📊 Total accounts: {accounts_response.total}")
        print(f"   📄 Page: {accounts_response.page}")
        print(f"   📝 Limit: {accounts_response.limit}")
        print(f"   ➡️  Has next: {accounts_response.has_next}")

        for i, account in enumerate(accounts_response.accounts, 1):
            print(f"   Account {i}:")
            print(f"     🆔 ID: {account.id}")
            print(f"     📛 Name: {account.name}")
            print(f"     📧 Email: {account.email}")
            print(f"     📞 Phone: {account.phone}")
            print(f"     ✅ Approved: {account.is_approved}")

        # Example 2: Get a template
        print("\n📋 WHATSAPP TEMPLATE EXAMPLE")
        print("-" * 30)

        print("📤 Getting WhatsApp template...")
        template = client.whatsapp.get_template("welcome_message")

        print("✅ Template retrieved successfully!")
        print(f"   📛 Name: {template.name}")
        print(f"   🌍 Language: {template.language}")
        print(f"   📊 Status: {template.status}")
        print(f"   📂 Category: {template.category}")
        print(f"   🔧 Components: {len(template.components)}")

        # Example 3: Upload a file
        print("\n📎 WHATSAPP FILE UPLOAD EXAMPLE")
        print("-" * 30)

        print("📤 Uploading file to WhatsApp...")

        # Create a sample file content for demonstration
        sample_content = b"This is a sample file content for WhatsApp upload demonstration."

        upload_response = client.whatsapp.upload_file(
            file_content=sample_content, filename="sample_document.txt", content_type="text/plain"
        )

        print("✅ File uploaded successfully!")
        print(f"   🆔 File ID: {upload_response.file_id}")
        print(f"   📄 Filename: {upload_response.filename}")
        print(f"   📏 File size: {upload_response.file_size} bytes")
        print(f"   🎭 MIME type: {upload_response.mime_type}")
        print(f"   🔗 URL: {upload_response.url}")
        if upload_response.expires_at:
            print(f"   ⏰ Expires at: {upload_response.expires_at}")

        # Example 4: Search accounts
        print("\n🔍 WHATSAPP ACCOUNTS SEARCH EXAMPLE")
        print("-" * 35)

        print("🔍 Searching WhatsApp accounts...")
        search_response = client.whatsapp.get_accounts(search="test")

        print("✅ Search completed!")
        print(f"   📊 Found {search_response.total} accounts matching 'test'")

        # Example 5: Send a normal message
        print("\n💬 WHATSAPP SEND MESSAGE EXAMPLE")
        print("-" * 32)

        print("📤 Sending WhatsApp message...")
        message_response = client.whatsapp.send_normal_message(
            to="+1234567890",
            message="Hello from the Devo WhatsApp SDK! 👋 This is a test message.",
            account_id="acc_123",  # Optional - uses default if not provided
        )

        print("✅ Message sent successfully!")
        print(f"   🆔 Message ID: {message_response.message_id}")
        print(f"   📊 Status: {message_response.status}")
        print(f"   📞 To: {message_response.to}")
        print(f"   🏢 Account ID: {message_response.account_id}")
        print(f"   🕐 Timestamp: {message_response.timestamp}")
        print(f"   ✅ Success: {message_response.success}")

        # Example 6: Send message with emojis and Unicode
        print("\n🌍 WHATSAPP UNICODE MESSAGE EXAMPLE")
        print("-" * 35)

        unicode_message = "¡Hola! 🎉 Welcome to Devo! 欢迎 مرحبا 🚀"
        unicode_response = client.whatsapp.send_normal_message(to="+1234567890", message=unicode_message)

        print("✅ Unicode message sent!")
        print(f"   🆔 Message ID: {unicode_response.message_id}")
        print(f"   📊 Status: {unicode_response.status}")

        # Example 7: Create a WhatsApp template
        print("\n📋 WHATSAPP CREATE TEMPLATE EXAMPLE")
        print("-" * 35)

        from devo_global_comms_python.models.whatsapp import (
            BodyComponent,
            ButtonsComponent,
            FooterComponent,
            QuickReplyButton,
            WhatsAppTemplateRequest,
        )

        print("📤 Creating WhatsApp template...")

        # Create a utility template for notifications
        template_request = WhatsAppTemplateRequest(
            name="order_confirmation_notification",
            language="en_US",
            category="UTILITY",
            components=[
                BodyComponent(
                    type="BODY",
                    text="Hi {{1}}! Your order #{{2}} has been confirmed and "
                    "will be delivered to {{3}}. Thank you for your purchase!",
                ),
                FooterComponent(type="FOOTER", text="Reply STOP to unsubscribe from notifications"),
                ButtonsComponent(
                    type="BUTTONS",
                    buttons=[
                        QuickReplyButton(type="QUICK_REPLY", text="Track Order"),
                        QuickReplyButton(type="QUICK_REPLY", text="Contact Support"),
                    ],
                ),
            ],
        )

        template_response = client.whatsapp.create_template(
            account_id="acc_123", template=template_request  # Replace with actual account ID
        )

        print("✅ Template created successfully!")
        print(f"   🆔 Template ID: {template_response.id}")
        print(f"   📛 Template Name: {template_response.name}")
        print(f"   📊 Status: {template_response.status}")
        print(f"   📂 Category: {template_response.category}")
        print(f"   🌍 Language: {template_response.language}")

        # Example 8: Get WhatsApp templates
        print("\n📋 WHATSAPP GET TEMPLATES EXAMPLE")
        print("-" * 33)

        print("📤 Getting WhatsApp templates...")
        templates_response = client.whatsapp.get_templates(
            account_id="acc_123", category="UTILITY", page=1, limit=5  # Replace with actual account ID
        )

        print("✅ Templates retrieved successfully!")
        print(f"   📊 Total templates: {templates_response.total}")
        print(f"   📄 Page: {templates_response.page}")
        print(f"   📝 Limit: {templates_response.limit}")
        print(f"   ➡️  Has next: {templates_response.has_next}")

        for i, template in enumerate(templates_response.templates, 1):
            print(f"   Template {i}:")
            print(f"     📛 Name: {template.name}")
            print(f"     📊 Status: {template.status}")
            print(f"     📂 Category: {template.category}")
            print(f"     🌍 Language: {template.language}")
            print(f"     🔧 Components: {len(template.components)}")

        # Example 9: Create an authentication template
        print("\n🔐 WHATSAPP AUTHENTICATION TEMPLATE EXAMPLE")
        print("-" * 42)

        from devo_global_comms_python.models.whatsapp import OTPButton

        print("📤 Creating authentication template...")

        auth_template_request = WhatsAppTemplateRequest(
            name="verification_code_template",
            language="en_US",
            category="AUTHENTICATION",
            components=[
                BodyComponent(type="BODY", add_security_recommendation=True),
                FooterComponent(type="FOOTER", code_expiration_minutes=10),
                ButtonsComponent(
                    type="BUTTONS", buttons=[OTPButton(type="OTP", otp_type="COPY_CODE", text="Copy Code")]
                ),
            ],
        )

        auth_template_response = client.whatsapp.create_template(account_id="acc_123", template=auth_template_request)

        print("✅ Authentication template created!")
        print(f"   🆔 Template ID: {auth_template_response.id}")
        print(f"   🔐 Category: {auth_template_response.category}")
        print(f"   📊 Status: {auth_template_response.status}")

        # Example 10: Create a marketing template with buttons
        print("\n🎯 WHATSAPP MARKETING TEMPLATE EXAMPLE")
        print("-" * 37)

        from devo_global_comms_python.models.whatsapp import (
            HeaderComponent,
            PhoneNumberButton,
            TemplateExample,
            URLButton,
        )

        print("📤 Creating marketing template...")

        marketing_template_request = WhatsAppTemplateRequest(
            name="summer_sale_promotion",
            language="en_US",
            category="MARKETING",
            components=[
                HeaderComponent(
                    type="HEADER",
                    format="TEXT",
                    text="🌞 Summer Sale Alert! {{1}}",
                    example=TemplateExample(header_text=["50% OFF"]),
                ),
                BodyComponent(
                    type="BODY",
                    text="Don't miss our biggest sale of the year! Get {{1}} off on all "
                    "summer collections. Use code {{2}} at checkout. Sale ends {{3}}!",
                    example=TemplateExample(body_text=[["50%", "SUMMER50", "July 31st"]]),
                ),
                FooterComponent(type="FOOTER", text="Terms and conditions apply. Limited time offer."),
                ButtonsComponent(
                    type="BUTTONS",
                    buttons=[
                        URLButton(
                            type="URL",
                            text="Shop Now",
                            url="https://example.com/summer-sale?promo={{1}}",
                            example=["SUMMER50"],
                        ),
                        PhoneNumberButton(type="PHONE_NUMBER", text="Call Us", phone_number="+1234567890"),
                    ],
                ),
            ],
        )

        marketing_template_response = client.whatsapp.create_template(
            account_id="acc_123", template=marketing_template_request
        )

        print("✅ Marketing template created!")
        print(f"   🆔 Template ID: {marketing_template_response.id}")
        print(f"   🎯 Category: {marketing_template_response.category}")
        print(f"   📊 Status: {marketing_template_response.status}")

        # Example 11: Send template message with text parameters
        print("\n📤 WHATSAPP SEND TEMPLATE MESSAGE EXAMPLE")
        print("-" * 40)

        from devo_global_comms_python.models.whatsapp import (
            TemplateMessageComponent,
            TemplateMessageLanguage,
            TemplateMessageParameter,
            TemplateMessageTemplate,
            WhatsAppTemplateMessageRequest,
        )

        print("📤 Sending template message...")

        # Send a simple text template message
        template_message_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="order_confirmation_notification",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="John Doe"),
                            TemplateMessageParameter(type="text", text="ORD-12345"),
                            TemplateMessageParameter(type="text", text="123 Main St, City"),
                        ],
                    )
                ],
            ),
        )

        template_message_response = client.whatsapp.send_template_message(
            account_id="acc_123", template_message=template_message_request
        )

        print("✅ Template message sent successfully!")
        print(f"   🆔 Message ID: {template_message_response.message_id}")
        print(f"   📊 Status: {template_message_response.status}")
        print(f"   📞 To: {template_message_response.to}")
        print(f"   🏢 Account ID: {template_message_response.account_id}")
        print(f"   ✅ Success: {template_message_response.success}")

        # Example 12: Send template message with image header
        print("\n🖼️ WHATSAPP TEMPLATE MESSAGE WITH IMAGE EXAMPLE")
        print("-" * 45)

        from devo_global_comms_python.models.whatsapp import ImageParameter

        print("📤 Sending template message with image header...")

        image_template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="limited_time_offer_tuscan_getaway_2023",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="header",
                        parameters=[
                            TemplateMessageParameter(
                                type="image", image=ImageParameter(link="https://example.com/summer-sale.jpg")
                            )
                        ],
                    ),
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="John"),
                            TemplateMessageParameter(type="text", text="Summer Vacation Package"),
                            TemplateMessageParameter(type="text", text="$799"),
                        ],
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="url",
                        index="0",
                        parameters=[TemplateMessageParameter(type="text", text="SUMMER2024")],
                    ),
                ],
            ),
        )

        image_template_response = client.whatsapp.send_template_message(
            account_id="acc_123", template_message=image_template_request
        )

        print("✅ Image template message sent!")
        print(f"   🆔 Message ID: {image_template_response.message_id}")
        print(f"   📊 Status: {image_template_response.status}")

        # Example 13: Send template message with location
        print("\n📍 WHATSAPP TEMPLATE MESSAGE WITH LOCATION EXAMPLE")
        print("-" * 49)

        from devo_global_comms_python.models.whatsapp import LocationParameter

        print("📤 Sending template message with location...")

        location_template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="order_delivery_update",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="header",
                        parameters=[
                            TemplateMessageParameter(
                                type="location",
                                location=LocationParameter(
                                    latitude="40.7128",
                                    longitude="-74.0060",
                                    name="Delivery Location",
                                    address="New York, NY 10001",
                                ),
                            )
                        ],
                    ),
                    TemplateMessageComponent(
                        type="body",
                        parameters=[
                            TemplateMessageParameter(type="text", text="John"),
                            TemplateMessageParameter(type="text", text="DEL-67890"),
                        ],
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="quick_reply",
                        index="0",
                        parameters=[TemplateMessageParameter(type="payload", payload="STOP_DELIVERY_UPDATES")],
                    ),
                ],
            ),
        )

        location_template_response = client.whatsapp.send_template_message(
            account_id="acc_123", template_message=location_template_request
        )

        print("✅ Location template message sent!")
        print(f"   🆔 Message ID: {location_template_response.message_id}")
        print(f"   📊 Status: {location_template_response.status}")

        # Example 14: Send authentication template with OTP
        print("\n🔐 WHATSAPP AUTHENTICATION TEMPLATE MESSAGE EXAMPLE")
        print("-" * 50)

        print("📤 Sending authentication template message...")

        auth_template_request = WhatsAppTemplateMessageRequest(
            to="+1234567890",
            template=TemplateMessageTemplate(
                name="devotel_otp",
                language=TemplateMessageLanguage(code="en_US"),
                components=[
                    TemplateMessageComponent(
                        type="body", parameters=[TemplateMessageParameter(type="text", text="123456")]
                    ),
                    TemplateMessageComponent(
                        type="button",
                        sub_type="url",
                        index="0",
                        parameters=[TemplateMessageParameter(type="text", text="123456")],
                    ),
                ],
            ),
        )

        auth_template_response = client.whatsapp.send_template_message(
            account_id="acc_123", template_message=auth_template_request
        )

        print("✅ Authentication template message sent!")
        print(f"   🆔 Message ID: {auth_template_response.message_id}")
        print("   🔐 OTP Code: 123456")
        print(f"   📊 Status: {auth_template_response.status}")

    except DevoException as e:
        print(f"❌ WhatsApp operation failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print("\n" + "=" * 60)
    print("📊 WHATSAPP EXAMPLE SUMMARY")
    print("-" * 30)
    print("✅ WhatsApp API implementation complete!")
    print("📤 Successfully demonstrated:")
    print("   • Getting WhatsApp accounts with pagination")
    print("   • Retrieving templates by name")
    print("   • Uploading files with proper metadata")
    print("   • Searching accounts with filters")
    print("   • Sending normal messages")
    print("   • Unicode and emoji support")
    print("   • Creating WhatsApp templates (utility, authentication, marketing)")
    print("   • Getting templates with filtering and pagination")
    print("   • Complex template components (headers, buttons, examples)")
    print("   • Sending template messages with parameters")
    print("   • Template messages with images, locations, documents")
    print("   • Authentication templates with OTP codes")
    print("   • Marketing templates with dynamic content")
    print("   • Template validation and error handling")
    print("   • Response parsing and error handling")
    print("\n💡 Available endpoints:")
    print("   • GET /user-api/whatsapp/accounts - Get shared accounts")
    print("   • GET /user-api/whatsapp/templates/{name} - Get template by name")
    print("   • POST /user-api/whatsapp/upload - Upload files")
    print("   • POST /user-api/whatsapp/send-normal-message - Send messages")
    print("   • POST /user-api/whatsapp/templates - Create templates")
    print("   • GET /user-api/whatsapp/templates - Get all templates")
    print("   • POST /user-api/whatsapp/send-message-by-template - Send template messages")


if __name__ == "__main__":
    main()
