from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..utils import validate_phone_number, validate_required_string
from .base import BaseResource

if TYPE_CHECKING:
    from ..models.whatsapp import (
        GetWhatsAppAccountsResponse,
        GetWhatsAppTemplatesResponse,
        WhatsAppMessage,
        WhatsAppSendMessageResponse,
        WhatsAppTemplate,
        WhatsAppTemplateMessageRequest,
        WhatsAppTemplateMessageResponse,
        WhatsAppTemplateRequest,
        WhatsAppTemplateResponse,
        WhatsAppUploadFileResponse,
    )


class WhatsAppResource(BaseResource):
    """
    WhatsApp resource for sending and managing WhatsApp messages.

    This resource provides access to WhatsApp functionality including:
    - Managing WhatsApp accounts
    - Getting templates
    - Uploading files
    - Sending messages

    Examples:
        Get accounts:
        >>> accounts = client.whatsapp.get_accounts()
        >>> for account in accounts.accounts:
        ...     print(f"Account: {account.name} (Approved: {account.is_approved})")

        Get template:
        >>> template = client.whatsapp.get_template("welcome_message")
        >>> print(f"Template: {template.name} ({template.status})")

        Upload file:
        >>> with open("image.jpg", "rb") as f:
        ...     upload = client.whatsapp.upload_file(f.read(), "image.jpg", "image/jpeg")
        >>> print(f"File uploaded: {upload.file_id}")
    """

    def get_accounts(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        is_approved: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> "GetWhatsAppAccountsResponse":
        """
        Get all shared WhatsApp accounts.

        Args:
            page: The page number (optional)
            limit: The page limit (optional)
            is_approved: Filter by approval status (optional)
            search: Search by name, email, phone (optional)

        Returns:
            GetWhatsAppAccountsResponse: List of WhatsApp accounts with pagination info

        Raises:
            DevoAPIException: If the API returns an error

        Example:
            >>> accounts = client.whatsapp.get_accounts(
            ...     page=1,
            ...     limit=10,
            ...     is_approved=True
            ... )
            >>> print(f"Found {accounts.total} accounts")
        """
        params = {}

        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if is_approved is not None:
            params["isApproved"] = is_approved
        if search is not None:
            params["search"] = search

        # Send request to the exact API endpoint
        response = self.client.get("user-api/whatsapp/accounts", params=params)

        from ..models.whatsapp import GetWhatsAppAccountsResponse

        return GetWhatsAppAccountsResponse.model_validate(response.json())

    def get_template(self, name: str) -> "WhatsAppTemplate":
        """
        Get a WhatsApp template by name.

        Args:
            name: Template name

        Returns:
            WhatsAppTemplate: The template details

        Raises:
            DevoValidationException: If the name is invalid
            DevoAPIException: If the API returns an error (404 if not found)

        Example:
            >>> template = client.whatsapp.get_template("welcome_message")
            >>> print(f"Template: {template.name}")
            >>> print(f"Status: {template.status}")
            >>> print(f"Components: {len(template.components)}")
        """
        name = validate_required_string(name, "name")

        # Send request to the exact API endpoint
        response = self.client.get(f"user-api/whatsapp/templates/{name}")

        from ..models.whatsapp import WhatsAppTemplate

        return WhatsAppTemplate.model_validate(response.json())

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
    ) -> "WhatsAppUploadFileResponse":
        """
        Upload a file for WhatsApp messaging.

        Args:
            file_content: The file content as bytes
            filename: Name of the file
            content_type: MIME type of the file

        Returns:
            WhatsAppUploadFileResponse: File upload details including file_id and URL

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error (400 for unsupported file type)

        Example:
            >>> with open("document.pdf", "rb") as f:
            ...     upload = client.whatsapp.upload_file(
            ...         f.read(),
            ...         "document.pdf",
            ...         "application/pdf"
            ...     )
            >>> print(f"File ID: {upload.file_id}")
            >>> print(f"URL: {upload.url}")
        """
        filename = validate_required_string(filename, "filename")
        content_type = validate_required_string(content_type, "content_type")

        if not file_content:
            from ..exceptions import DevoValidationException

            raise DevoValidationException("File content cannot be empty")

        # Prepare multipart form data
        files = {
            "file": (filename, file_content, content_type),
        }

        # Send request to the exact API endpoint
        response = self.client.post("user-api/whatsapp/upload", files=files)

        from ..models.whatsapp import WhatsAppUploadFileResponse

        return WhatsAppUploadFileResponse.model_validate(response.json())

    def send_normal_message(
        self,
        to: str,
        message: str,
        account_id: Optional[str] = None,
    ) -> "WhatsAppSendMessageResponse":
        """
        Send a normal WhatsApp message.

        Args:
            to: Recipient phone number in E.164 format
            message: Message content
            account_id: WhatsApp account ID to send from (optional)

        Returns:
            WhatsAppSendMessageResponse: The message send response

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> response = client.whatsapp.send_normal_message(
            ...     to="+1234567890",
            ...     message="Hello from WhatsApp!",
            ...     account_id="acc_123"
            ... )
            >>> print(f"Message ID: {response.message_id}")
            >>> print(f"Status: {response.status}")
        """
        # Validate inputs
        to = validate_phone_number(to)
        message = validate_required_string(message, "message")

        # Prepare request data according to API spec
        from ..models.whatsapp import WhatsAppNormalMessageRequest

        request_data = WhatsAppNormalMessageRequest(
            to=to,
            message=message,
            account_id=account_id,
        )

        # Send request to the exact API endpoint
        response = self.client.post(
            "user-api/whatsapp/send-normal-message", json=request_data.model_dump(exclude_none=True)
        )

        from ..models.whatsapp import WhatsAppSendMessageResponse

        return WhatsAppSendMessageResponse.model_validate(response.json())

    def create_template(
        self,
        account_id: str,
        template: "WhatsAppTemplateRequest",
    ) -> "WhatsAppTemplateResponse":
        """
        Create a WhatsApp template.

        Args:
            account_id: WhatsApp account ID
            template: Template creation request data

        Returns:
            WhatsAppTemplateResponse: The created template

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> from ..models.whatsapp import (
            ...     WhatsAppTemplateRequest,
            ...     BodyComponent,
            ...     FooterComponent
            ... )
            >>> template_request = WhatsAppTemplateRequest(
            ...     name="welcome_message",
            ...     language="en_US",
            ...     category="UTILITY",
            ...     components=[
            ...         BodyComponent(type="BODY", text="Welcome to our service!"),
            ...         FooterComponent(type="FOOTER", text="Thank you for choosing us")
            ...     ]
            ... )
            >>> response = client.whatsapp.create_template(
            ...     account_id="acc_123",
            ...     template=template_request
            ... )
            >>> print(f"Template ID: {response.id}")
        """
        # Validate inputs
        account_id = validate_required_string(account_id, "account_id")

        # Prepare query parameters
        params = {"account_id": account_id}

        # Send request to the exact API endpoint
        response = self.client.post(
            "user-api/whatsapp/templates", params=params, json=template.model_dump(exclude_none=True)
        )

        from ..models.whatsapp import WhatsAppTemplateResponse

        return WhatsAppTemplateResponse.model_validate(response.json())

    def get_templates(
        self,
        account_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> "GetWhatsAppTemplatesResponse":
        """
        Get WhatsApp templates for an account.

        Args:
            account_id: WhatsApp account ID (required)
            page: Page number for pagination (optional)
            limit: Number of templates per page (optional)
            category: Filter by template category (AUTHENTICATION, MARKETING, UTILITY)
            search: Search templates by name (optional)

        Returns:
            GetWhatsAppTemplatesResponse: Paginated list of templates

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> response = client.whatsapp.get_templates(
            ...     account_id="acc_123",
            ...     category="MARKETING",
            ...     page=1,
            ...     limit=10
            ... )
            >>> print(f"Found {response.total} templates")
            >>> for template in response.templates:
            ...     print(f"Template: {template.name}")
        """
        # Validate inputs
        account_id = validate_required_string(account_id, "account_id")

        # Prepare query parameters
        params = {"id": account_id}  # Note: API uses 'id' parameter name for account_id

        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if category is not None:
            # Validate category enum
            valid_categories = ["AUTHENTICATION", "MARKETING", "UTILITY"]
            if category not in valid_categories:
                from ..exceptions import DevoValidationException

                raise DevoValidationException(
                    f"Invalid category '{category}'. Must be one of: {', '.join(valid_categories)}"
                )
            params["category"] = category
        if search is not None:
            params["search"] = search

        # Send request to the exact API endpoint
        response = self.client.get("user-api/whatsapp/templates", params=params)

        from ..models.whatsapp import GetWhatsAppTemplatesResponse

        return GetWhatsAppTemplatesResponse.model_validate(response.json())

    def send_template_message(
        self,
        account_id: str,
        template_message: "WhatsAppTemplateMessageRequest",
    ) -> "WhatsAppTemplateMessageResponse":
        """
        Send a WhatsApp template message.

        Args:
            account_id: WhatsApp account ID
            template_message: Template message request data

        Returns:
            WhatsAppTemplateMessageResponse: The message send response

        Raises:
            DevoValidationException: If required fields are invalid
            DevoAPIException: If the API returns an error

        Example:
            >>> from ..models.whatsapp import (
            ...     WhatsAppTemplateMessageRequest,
            ...     TemplateMessageTemplate,
            ...     TemplateMessageLanguage,
            ...     TemplateMessageComponent,
            ...     TemplateMessageParameter
            ... )
            >>> # Simple text template message
            >>> template_request = WhatsAppTemplateMessageRequest(
            ...     to="+1234567890",
            ...     template=TemplateMessageTemplate(
            ...         name="welcome_message",
            ...         language=TemplateMessageLanguage(code="en_US"),
            ...         components=[
            ...             TemplateMessageComponent(
            ...                 type="body",
            ...                 parameters=[
            ...                     TemplateMessageParameter(
            ...                         type="text",
            ...                         text="John Doe"
            ...                     )
            ...                 ]
            ...             )
            ...         ]
            ...     )
            ... )
            >>> response = client.whatsapp.send_template_message(
            ...     account_id="acc_123",
            ...     template_message=template_request
            ... )
            >>> print(f"Message ID: {response.message_id}")
        """
        # Validate inputs
        account_id = validate_required_string(account_id, "account_id")

        # Prepare query parameters
        params = {"account_id": account_id}

        # Send request to the exact API endpoint
        response = self.client.post(
            "user-api/whatsapp/send-message-by-template",
            params=params,
            json=template_message.model_dump(exclude_none=True),
        )

        from ..models.whatsapp import WhatsAppTemplateMessageResponse

        return WhatsAppTemplateMessageResponse.model_validate(response.json())

    def send_text(
        self,
        to: str,
        text: str,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "WhatsAppMessage":
        """Send a WhatsApp text message."""
        to = validate_phone_number(to)
        text = validate_required_string(text, "text")

        data = {"to": to, "type": "text", "text": {"body": text}}
        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("whatsapp/messages", json=data)

        from ..models.whatsapp import WhatsAppMessage

        return WhatsAppMessage.model_validate(response.json())

    def send_template(
        self,
        to: str,
        template_name: str,
        language: str = "en",
        parameters: Optional[List[str]] = None,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "WhatsAppMessage":
        """Send a WhatsApp template message."""
        to = validate_phone_number(to)
        template_name = validate_required_string(template_name, "template_name")

        data = {
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language},
            },
        }

        if parameters:
            data["template"]["components"] = [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": p} for p in parameters],
                }
            ]

        if callback_url:
            data["callback_url"] = callback_url
        if metadata:
            data["metadata"] = metadata

        response = self.client.post("whatsapp/messages", json=data)

        from ..models.whatsapp import WhatsAppMessage

        return WhatsAppMessage.model_validate(response.json())

    def get(self, message_id: str) -> "WhatsAppMessage":
        """Retrieve a WhatsApp message by ID."""
        message_id = validate_required_string(message_id, "message_id")
        response = self.client.get(f"whatsapp/messages/{message_id}")

        from ..models.whatsapp import WhatsAppMessage

        return WhatsAppMessage.model_validate(response.json())
