#!/bin/bash

# Verify Ollama configuration is properly loaded

echo "=== Ollama Configuration Verification ==="

# Check if environment file exists
if [ -f "ollama.env" ]; then
    echo "✓ ollama.env file found"
    echo "Contents:"
    cat ollama.env
else
    echo "✗ ollama.env file not found"
    exit 1
fi

echo ""
echo "=== Environment Variables ==="
echo "Loading environment..."
export $(cat ollama.env)
echo "OLLAMA_HOST: $OLLAMA_HOST"
echo "OLLAMA_KEEP_ALIVE: $OLLAMA_KEEP_ALIVE"
echo "OLLAMA_CONTEXT_LENGTH: $OLLAMA_CONTEXT_LENGTH"
echo "OLLAMA_NUM_PARALLEL: $OLLAMA_NUM_PARALLEL"
echo "OLLAMA_MAX_LOADED_MODELS: $OLLAMA_MAX_LOADED_MODELS"
echo "OLLAMA_KV_CACHE_TYPE: $OLLAMA_KV_CACHE_TYPE"

echo ""
echo "=== Model Availability ==="
ollama list | grep -E "(gemma|all-minilm)"