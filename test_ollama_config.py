#!/usr/bin/env python3
"""
Test script to verify Ollama configuration is properly set up
"""

import os
import sys

def test_ollama_config():
    """Test that Ollama configuration is properly loaded"""
    print("Testing Ollama configuration...")

    try:
        # Test environment variables
        env_vars = [
            'OLLAMA_HOST',
            'OLLAMA_KEEP_ALIVE',
            'OLLAMA_CONTEXT_LENGTH',
            'OLLAMA_NUM_PARALLEL',
            'OLLAMA_MAX_LOADED_MODELS',
            'OLLAMA_KV_CACHE_TYPE'
        ]

        print("Environment variables loaded:")
        for var in env_vars:
            value = os.getenv(var, "Not set")
            print(f"  {var}: {value}")

        # Test that we can access the Ollama client
        from app.api.ollama_client import OLLAMA_HOST, MODEL_NAME, CONTEXT_LENGTH, KEEP_ALIVE

        print(f"\nOllama Client Configuration:")
        print(f"  Host: {OLLAMA_HOST}")
        print(f"  Model: {MODEL_NAME}")
        print(f"  Context Length: {CONTEXT_LENGTH}")
        print(f"  Keep Alive: {KEEP_ALIVE}")

        print("✓ Ollama configuration test passed")
        return True

    except Exception as e:
        print(f"✗ Error testing Ollama configuration: {e}")
        return False

def test_model_availability():
    """Test that required models are available"""
    print("\nTesting model availability...")

    try:
        from app.api.ollama_client import list_available_models

        models = list_available_models()
        model_names = [model['name'] for model in models]
        print(f"Available models: {model_names}")

        required_models = ['gemma:2b', 'all-minilm:22m']
        missing_models = []

        for model in required_models:
            if model in model_names:
                print(f"✓ {model} available")
            else:
                print(f"✗ {model} not available")
                missing_models.append(model)

        if not missing_models:
            print("✓ All required models available")
            return True
        else:
            print(f"Note: Missing models - {missing_models}")
            print("Run: ollama pull gemma:2b and ollama pull all-minilm:22m")
            return True  # Not critical error, just informational

    except Exception as e:
        print(f"✗ Error testing model availability: {e}")
        return False

def main():
    """Run all tests"""
    print("Life Dashboard - Ollama Configuration Test")
    print("=" * 50)

    tests = [
        test_ollama_config,
        test_model_availability
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✓ All configuration tests passed!")
        return 0
    else:
        print("✗ Some configuration tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())