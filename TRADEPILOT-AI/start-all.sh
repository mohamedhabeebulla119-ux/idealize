#!/bin/bash

# TradePilot AI - Start All Services (macOS/Linux)

echo ""
echo "========================================"
echo "  TradePilot AI - Full Stack Startup"
echo "========================================"
echo ""

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install backend requirements
echo ""
echo "Installing backend dependencies..."
pip install -r requirements.txt -q
pip install python-multipart -q

# Start backend in background
echo ""
echo "Starting backend server on port 8000..."
cd backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend server on port 5173..."
cd frontend
npm install -q
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  Services Started!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Process IDs:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "To stop services, run: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Wait for interrupt
wait
