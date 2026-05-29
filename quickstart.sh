#!/bin/bash
#
# Sentinel Red Team - Quick Start Script
#

echo "=================================="
echo "Sentinel Red Team - Quick Start"
echo "=================================="
echo

# Check Python version
echo "[1/6] Checking Python version..."
python3 --version || { echo "Error: Python 3 not found"; exit 1; }
echo "✓ Python 3 found"
echo

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo

# Install dependencies
echo "[4/6] Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"
echo

# Check for API key
echo "[5/6] Checking for API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo
    echo "Please set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo
    echo "Or create a .env file:"
    echo "  echo 'ANTHROPIC_API_KEY=your-key-here' > .env"
    echo
    read -p "Do you want to enter your API key now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Anthropic API key: " api_key
        export ANTHROPIC_API_KEY="$api_key"
        echo "ANTHROPIC_API_KEY=$api_key" > .env
        echo "✓ API key saved to .env"
    else
        echo "⚠️  You'll need to set ANTHROPIC_API_KEY before running Sentinel"
    fi
else
    echo "✓ API key found"
fi
echo

# Create necessary directories
echo "[6/6] Creating directories..."
mkdir -p logs knowledge reports
echo "✓ Directories created"
echo

echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo
echo "To start Sentinel:"
echo "  source venv/bin/activate"
echo "  python sentinel.py"
echo
echo "For help:"
echo "  python sentinel.py --help"
echo
echo "First time? Read SETUP.md for detailed instructions"
echo
