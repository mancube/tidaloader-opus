#!/data/data/com.termux/files/usr/bin/bash

# Restart script for Tidal Troi UI
cd ~/tidaloader
./stop-service.sh
sleep 2
./start-service.sh