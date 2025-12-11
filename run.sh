#!/bin/bash

# Anomaly Report Analyzer - Master Launch Script (Linux/Mac)

echo ""
echo "================================================================================"
echo "  ANOMALY REPORT ANALYZER - SYSTEM LAUNCHER"
echo "================================================================================"
echo ""

# Check if Node.js is installed
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js is not installed"; exit 1; }
echo "✓ Node.js found"

# Check if Python is installed
command -v python3 >/dev/null 2>&1 || { echo "ERROR: Python is not installed"; exit 1; }
echo "✓ Python found"
echo ""

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"

# Install/update Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"

# Install frontend dependencies
echo ""
echo "Installing frontend dependencies..."
cd frontend
npm install --silent
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install frontend dependencies"
    cd ..
    exit 1
fi
echo "✓ Frontend dependencies installed"
cd ..

# Display startup information
echo ""
echo "================================================================================"
echo "  STARTING SERVICES"
echo "================================================================================"
echo ""
echo "FRONTEND:  http://localhost:3001"
echo "BACKEND:   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""
echo "================================================================================"
echo ""

# Start backend in background
echo "Starting Backend Server..."
python app.py &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Start frontend
echo "Starting Frontend Server..."
cd frontend
npm start

# Wait for frontend
wait

# Kill backend when frontend exits
kill $BACKEND_PID 2>/dev/null

exit 0
