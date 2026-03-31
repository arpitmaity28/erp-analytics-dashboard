#!/bin/bash

# ERP Analytics Dashboard Quick Start Script

echo "=========================================="
echo "ERP Analytics Dashboard - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install/upgrade dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Run tests
echo ""
echo "Running validation tests..."
python test_erp.py | tail -20

# Start Streamlit
echo ""
echo "=========================================="
echo "Starting Streamlit Dashboard..."
echo "=========================================="
echo ""
echo "Dashboard will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
