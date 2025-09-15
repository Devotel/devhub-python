# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-09-15

### Added
- Initial release of DevHub Python SDK
- Multi-channel communication support (SMS, Email, WhatsApp, RCS)
- Contact management functionality
- Contact groups management
- Sandbox environment support
- Comprehensive test suite (185+ tests)
- Type safety with Pydantic models
- Full documentation with MkDocs

### Features
- **SMS**: Send messages, manage senders, buy numbers
- **Email**: Send HTML/plain text emails with attachments
- **WhatsApp**: Send text, template, and media messages
- **RCS**: Rich messaging with cards, suggestions, and media
- **Contacts**: CRUD operations, custom fields, CSV import
- **Contact Groups**: Group management and bulk operations
- **Authentication**: API key and sandbox API key support
- **Error Handling**: Comprehensive exception hierarchy
- **Validation**: Phone numbers, emails, and request validation

### Technical
- Python 3.8+ support
- Minimal dependencies (requests, pydantic)
- Pre-commit hooks for code quality
- MkDocs documentation with GitHub Pages

## [Unreleased]
- Future enhancements and bug fixes will be listed here
