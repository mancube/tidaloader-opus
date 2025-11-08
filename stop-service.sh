#!/data/data/com.termux/files/usr/bin/bash

# Stop script for Tidal Troi UI
if [ -f ~/tidaloader.pid ]; then
    PID=$(cat ~/tidaloader.pid)
    if kill -0 $PID 2>/dev/null; then
        echo "Stopping Tidal Troi UI (PID: $PID)..."
        kill $PID
        rm ~/tidaloader.pid
        echo "Service stopped"
    else
        echo "Process not running"
        rm ~/tidaloader.pid
    fi
else
    echo "PID file not found"
fi