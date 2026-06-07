#!/bin/bash

echo "========================================"
echo "  OpenAll-In-AI - Starting Frontend"
echo "========================================"
echo

cd "$(dirname "$0")/../frontend"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 18+"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Starting frontend development server..."
npm run dev