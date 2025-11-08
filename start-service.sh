#!/data/data/com.termux/files/usr/bin/bash

# Start script for Tidal Troi UI
set -e

cd ~/tidaloader/backend

# Activate virtual environment
source venv/bin/activate

# Start the backend server
echo "Starting Tidal Troi UI backend on port 8001..."
nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 > ~/tidaloader.log 2>&1 &

echo $! > ~/tidaloader.pid
echo "Service started with PID $(cat ~/tidaloader.pid)"
echo "Logs: ~/tidaloader.log"
echo "Access at: http://localhost:8001"