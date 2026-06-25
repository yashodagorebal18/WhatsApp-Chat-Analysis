#!/bin/bash

# Startup script for WhatsApp Chat Analyzer
# This script starts both the Flask backend and Streamlit frontend

echo ""
echo "========================================"
echo "  WhatsApp Chat Analyzer - Full Stack"
echo "  Version 2.0.0"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Download NLTK data if needed
echo "Setting up NLP resources..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)" 2>/dev/null

echo ""
echo "========================================"
echo "  Starting Application"
echo "========================================"
echo ""

# Start Flask Backend in background
echo "Starting Flask Backend (Port 5000)..."
python api_backend.py &
BACKEND_PID=$!

# Wait a moment for Flask to start
sleep 3

# Start Streamlit Frontend
echo "Starting Streamlit Frontend (Port 8501)..."
echo "Opening browser at http://localhost:8501"
streamlit run app_enhanced.py

# Cleanup
kill $BACKEND_PID 2>/dev/null
