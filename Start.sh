#!/bin/bash

echo "========================================"
echo "  OpenAll-In-AI - One-Click Start"
echo "========================================"
echo

cd "$(dirname "$0")"

# Start backend in background
echo "Starting Backend Server..."
./scripts/start_backend.sh &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend in background
echo "Starting Frontend Server..."
./scripts/start_frontend.sh &
FRONTEND_PID=$!

echo
echo "========================================"
echo "  Both servers are starting!"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "========================================"
echo

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID