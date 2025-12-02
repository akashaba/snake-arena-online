#!/bin/bash

# Start both backend and frontend servers
# Run this from the root directory

echo "🚀 Starting Neon Snake Arena servers..."
echo ""

# Start backend in background
echo "📦 Starting Backend (http://localhost:8000)..."
cd backend
uv run python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start frontend in background
echo "🎮 Starting Frontend (http://localhost:8080)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers started!"
echo ""
echo "Backend API: http://localhost:8000/docs"
echo "Frontend:    http://localhost:8080"
echo ""
echo "Test credentials:"
echo "  Email:    neon@example.com"
echo "  Password: password123"
echo ""
echo "Press Ctrl+C to stop both servers"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Wait for processes
wait
