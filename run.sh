#!/bin/bash

# Simple script to start the Life Dashboard application

# Load Ollama configuration
echo "Loading Ollama configuration..."
export $(cat ollama.env)

# Check if Ollama is already running
if pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama is already running - using existing instance"
else
    echo "Starting Ollama server..."
    ollama serve &
    # Wait for Ollama to start
    echo "Waiting for Ollama to initialize..."
    sleep 5
fi

# Activate virtual environment
source lifedashboard-env/bin/activate

# Start the application
echo "Starting Life Dashboard..."
uvicorn app.main:app --host 0.0.0.0 --port 8001