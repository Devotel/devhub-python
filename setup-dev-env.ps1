#!/usr/bin/env powershell
# Development Environment Setup Script for Devo Global Communications Python SDK

Write-Host "🚀 Setting up Devo Global Communications Python SDK development environment..."
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "pyproject.toml")) {
    Write-Host "❌ Error: pyproject.toml not found. Please run this script from the project root directory."
    exit 1
}

# Create virtual environment if it doesn't exist
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..."
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Failed to create virtual environment."
        exit 1
    }
} else {
    Write-Host "✓ Virtual environment already exists"
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "⬆️ Upgrading pip..."
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Failed to upgrade pip."
    exit 1
}

# Install package in development mode with all dependencies
Write-Host "📚 Installing package and dependencies..."
pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Failed to install package and dependencies."
    exit 1
}

# Initialize git if not already done
if (!(Test-Path ".git")) {
    Write-Host "🔄 Initializing git repository..."
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Warning: Git initialization failed. You may need to install Git."
    }
}

# Install pre-commit hooks
Write-Host "🪝 Installing pre-commit hooks..."
pre-commit install
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Warning: Pre-commit hooks installation failed."
}

# Verify installation
Write-Host ""
Write-Host "🧪 Testing installation..."
python -c "from devo_global_comms_python import DevoClient; print('✓ SDK import successful')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: SDK import test failed."
    exit 1
}

python -c "from devo_global_comms_python import DevoClient; client = DevoClient('test-key'); print('✓ Client initialization successful')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Client initialization test failed."
    exit 1
}

Write-Host ""
Write-Host "🎉 Development environment setup complete!"
Write-Host ""
Write-Host "📋 Next steps:"
Write-Host "  1. Activate virtual environment: .\venv\Scripts\Activate.ps1"
Write-Host "  2. Run tests: pytest"
Write-Host "  3. Format code: black src/ tests/"
Write-Host "  4. Check types: mypy src/"
Write-Host "  5. Run linting: flake8 src/"
Write-Host ""
Write-Host "📚 Useful commands:"
Write-Host "  • Run tests with coverage: pytest --cov"
Write-Host "  • Format and sort imports: black src/ tests/ && isort src/ tests/"
Write-Host "  • Run all quality checks: pre-commit run --all-files"
Write-Host ""
Write-Host "Happy coding! 🚀"
