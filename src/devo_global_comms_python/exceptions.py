from typing import Any, Dict, Optional

import requests


class DevoException(Exception):
    """
    Base exception for all Devo SDK errors.

    All exceptions in the SDK inherit from this class.
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        self.message = message
        self.details = details or {}
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


# HTTP-Related Exceptions


class DevoAPIException(DevoException):
    """
    Base exception for API-related errors.

    Includes HTTP response details and error codes.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        response: Optional[requests.Response] = None,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, details)
        self.status_code = status_code
        self.error_code = error_code
        self.response = response
        self.request_id = request_id

        # Extract request details for debugging
        self.request_details = {}
        if response is not None and hasattr(response, "request"):
            try:
                self.request_details = {
                    "method": response.request.method,
                    "url": response.request.url,
                    "headers": dict(response.request.headers) if hasattr(response.request, "headers") else {},
                }
            except (AttributeError, TypeError):
                # Handle cases where response is mocked or doesn't have expected attributes
                self.request_details = {
                    "method": getattr(response.request, "method", "UNKNOWN"),
                    "url": getattr(response.request, "url", "UNKNOWN"),
                    "headers": {},
                }

    def __str__(self) -> str:
        parts = []

        if self.status_code:
            parts.append(f"[{self.status_code}]")

        if self.error_code:
            parts.append(f"{self.error_code}")

        parts.append(self.message)

        if self.request_id:
            parts.append(f"(Request ID: {self.request_id})")

        return " ".join(parts)


class DevoBadRequestException(DevoAPIException):
    """Exception raised for 400 Bad Request errors."""

    def __init__(self, message: str = "Bad Request", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class DevoAuthenticationException(DevoAPIException):
    """Exception raised for 401 Unauthorized errors."""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class DevoForbiddenException(DevoAPIException):
    """Exception raised for 403 Forbidden errors."""

    def __init__(self, message: str = "Access forbidden", **kwargs):
        super().__init__(message, status_code=403, **kwargs)


class DevoNotFoundException(DevoAPIException):
    """Exception raised for 404 Not Found errors."""

    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class DevoMethodNotAllowedException(DevoAPIException):
    """Exception raised for 405 Method Not Allowed errors."""

    def __init__(self, message: str = "Method not allowed", **kwargs):
        super().__init__(message, status_code=405, **kwargs)


class DevoConflictException(DevoAPIException):
    """Exception raised for 409 Conflict errors."""

    def __init__(self, message: str = "Conflict", **kwargs):
        super().__init__(message, status_code=409, **kwargs)


class DevoUnprocessableEntityException(DevoAPIException):
    """Exception raised for 422 Unprocessable Entity errors."""

    def __init__(self, message: str = "Unprocessable entity", **kwargs):
        super().__init__(message, status_code=422, **kwargs)


class DevoRateLimitException(DevoAPIException):
    """
    Exception raised when rate limit is exceeded (429).

    Includes retry-after information when available.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining

    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after:
            base += f" (Retry after {self.retry_after} seconds)"
        return base


class DevoInternalServerException(DevoAPIException):
    """Exception raised for 500 Internal Server Error."""

    def __init__(self, message: str = "Internal server error", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


class DevoBadGatewayException(DevoAPIException):
    """Exception raised for 502 Bad Gateway errors."""

    def __init__(self, message: str = "Bad gateway", **kwargs):
        super().__init__(message, status_code=502, **kwargs)


class DevoServiceUnavailableException(DevoAPIException):
    """Exception raised for 503 Service Unavailable errors."""

    def __init__(self, message: str = "Service unavailable", **kwargs):
        super().__init__(message, status_code=503, **kwargs)


class DevoGatewayTimeoutException(DevoAPIException):
    """Exception raised for 504 Gateway Timeout errors."""

    def __init__(self, message: str = "Gateway timeout", **kwargs):
        super().__init__(message, status_code=504, **kwargs)


# Business Logic Exceptions


class DevoValidationException(DevoException):
    """
    Exception raised for validation errors.

    Used when input data doesn't meet requirements.
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value

    def __str__(self) -> str:
        if self.field:
            return f"Validation error for field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"


class DevoInvalidPhoneNumberException(DevoValidationException):
    """Exception raised for invalid phone numbers."""

    def __init__(self, phone_number: str, **kwargs):
        message = f"Invalid phone number format: {phone_number}. Must be in E.164 format (e.g., +1234567890)"
        super().__init__(message, field="phone_number", value=phone_number, **kwargs)


class DevoInvalidEmailException(DevoValidationException):
    """Exception raised for invalid email addresses."""

    def __init__(self, email: str, **kwargs):
        message = f"Invalid email address format: {email}"
        super().__init__(message, field="email", value=email, **kwargs)


class DevoTemplateNotFoundException(DevoNotFoundException):
    """Exception raised when a message template is not found."""

    def __init__(self, template_name: str, **kwargs):
        message = f"Template not found: {template_name}"
        super().__init__(message, **kwargs)
        self.template_name = template_name


class DevoContactNotFoundException(DevoNotFoundException):
    """Exception raised when a contact is not found."""

    def __init__(self, contact_id: str, **kwargs):
        message = f"Contact not found: {contact_id}"
        super().__init__(message, **kwargs)
        self.contact_id = contact_id


class DevoMessageNotFoundException(DevoNotFoundException):
    """Exception raised when a message is not found."""

    def __init__(self, message_id: str, **kwargs):
        message = f"Message not found: {message_id}"
        super().__init__(message, **kwargs)
        self.message_id = message_id


class DevoInsufficientCreditsException(DevoAPIException):
    """Exception raised when account has insufficient credits."""

    def __init__(
        self,
        required: Optional[float] = None,
        available: Optional[float] = None,
        **kwargs,
    ):
        if required and available:
            message = f"Insufficient credits. Required: {required}, Available: {available}"
        else:
            message = "Insufficient credits to complete this operation"
        super().__init__(message, status_code=402, **kwargs)
        self.required = required
        self.available = available


class DevoMessageTooLongException(DevoValidationException):
    """Exception raised when message content exceeds length limits."""

    def __init__(self, length: int, max_length: int, **kwargs):
        message = f"Message too long. Length: {length}, Maximum: {max_length}"
        super().__init__(message, field="body", **kwargs)
        self.length = length
        self.max_length = max_length


class DevoUnsupportedChannelException(DevoException):
    """Exception raised when trying to use an unsupported channel."""

    def __init__(self, channel: str, **kwargs):
        message = f"Unsupported channel: {channel}"
        super().__init__(message, **kwargs)
        self.channel = channel


class DevoChannelNotEnabledException(DevoForbiddenException):
    """Exception raised when trying to use a channel that's not enabled for the account."""

    def __init__(self, channel: str, **kwargs):
        message = f"Channel not enabled for your account: {channel}"
        super().__init__(message, **kwargs)
        self.channel = channel


# Network Exceptions


class DevoNetworkException(DevoException):
    """Base exception for network-related errors."""

    pass


class DevoTimeoutException(DevoNetworkException):
    """Exception raised for timeout errors."""

    def __init__(self, timeout: Optional[float] = None, **kwargs):
        if timeout:
            message = f"Request timed out after {timeout} seconds"
        else:
            message = "Request timed out"
        super().__init__(message, **kwargs)
        self.timeout = timeout


class DevoConnectionException(DevoNetworkException):
    """Exception raised for connection errors."""

    def __init__(self, message: str = "Connection error", **kwargs):
        super().__init__(message, **kwargs)


class DevoDNSException(DevoConnectionException):
    """Exception raised for DNS resolution errors."""

    def __init__(self, hostname: Optional[str] = None, **kwargs):
        if hostname:
            message = f"DNS resolution failed for hostname: {hostname}"
        else:
            message = "DNS resolution failed"
        super().__init__(message, **kwargs)
        self.hostname = hostname


class DevoSSLException(DevoConnectionException):
    """Exception raised for SSL/TLS errors."""

    def __init__(self, message: str = "SSL/TLS error", **kwargs):
        super().__init__(message, **kwargs)


# Configuration Exceptions


class DevoConfigurationException(DevoException):
    """Base exception for configuration-related errors."""

    pass


class DevoMissingAPIKeyException(DevoConfigurationException):
    """Exception raised when API key is missing."""

    def __init__(self, **kwargs):
        message = "API key is required but not provided"
        super().__init__(message, **kwargs)


class DevoInvalidAPIKeyException(DevoAuthenticationException):
    """Exception raised when API key is invalid."""

    def __init__(self, **kwargs):
        message = "Invalid API key provided"
        super().__init__(message, **kwargs)


class DevoInvalidConfigurationException(DevoConfigurationException):
    """Exception raised for invalid configuration values."""

    def __init__(self, parameter: str, value: Any, reason: str, **kwargs):
        message = f"Invalid configuration for '{parameter}': {reason} (value: {value})"
        super().__init__(message, **kwargs)
        self.parameter = parameter
        self.value = value
        self.reason = reason


# Exception Factory


def create_exception_from_response(response: requests.Response) -> DevoAPIException:
    """
    Create an appropriate exception from an HTTP response.

    Args:
        response: The HTTP response object

    Returns:
        DevoAPIException: An appropriate exception subclass
    """
    status_code = response.status_code

    try:
        error_data = response.json()
        message = error_data.get("message", "Unknown error")
        error_code = error_data.get("code")
        request_id = error_data.get("request_id")
    except (ValueError, KeyError):
        message = response.text or f"HTTP {status_code}"
        error_code = None
        request_id = None

    # Extract rate limit headers
    retry_after: Optional[int] = None
    limit: Optional[int] = None
    remaining: Optional[int] = None

    if status_code == 429:
        retry_after_str = response.headers.get("Retry-After")
        if retry_after_str:
            try:
                retry_after = int(retry_after_str)
            except ValueError:
                retry_after = None

        limit_str = response.headers.get("X-RateLimit-Limit")
        if limit_str:
            try:
                limit = int(limit_str)
            except ValueError:
                limit = None

        remaining_str = response.headers.get("X-RateLimit-Remaining")
        if remaining_str:
            try:
                remaining = int(remaining_str)
            except ValueError:
                remaining = None

    # Map status codes to specific exceptions
    exception_map = {
        400: DevoBadRequestException,
        401: DevoAuthenticationException,
        403: DevoForbiddenException,
        404: DevoNotFoundException,
        405: DevoMethodNotAllowedException,
        409: DevoConflictException,
        422: DevoUnprocessableEntityException,
        429: DevoRateLimitException,
        500: DevoInternalServerException,
        502: DevoBadGatewayException,
        503: DevoServiceUnavailableException,
        504: DevoGatewayTimeoutException,
    }

    exception_class = exception_map.get(status_code, DevoAPIException)

    kwargs = {
        "message": message,
        "error_code": error_code,
        "response": response,
        "request_id": request_id,
    }

    # Add rate limit specific parameters
    if status_code == 429:
        kwargs.update(
            {
                "retry_after": retry_after,
                "limit": limit,
                "remaining": remaining,
            }
        )

    return exception_class(**kwargs)
