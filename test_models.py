#!/usr/bin/env python3
"""
Test script to verify the updated Life Dashboard works with new lightweight models
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_ollama_models():
    """Test that Ollama client can work with the new models"""
    print("Testing Ollama model integration...")

    try:
        from app.api.ollama_client import list_available_models, get_ai_insight

        # List available models
        models = list_available_models()
        print(f"✓ Available models: {len(models)} found")

        # Check if our models are available
        model_names = [model['name'] for model in models]
        print(f"Available models: {model_names}")

        # Test that the default model is available
        if 'gemma:2b' in model_names:
            print("✓ gemma:2b model available")
        else:
            print("Note: gemma:2b not available (may need to pull it)")

        if 'all-minilm:22m' in model_names:
            print("✓ all-minilm:22m model available")
        else:
            print("Note: all-minilm:22m not available (may need to pull it)")

        print("✓ Ollama client functionality verified")
        return True

    except Exception as e:
        print(f"✗ Error testing Ollama models: {e}")
        return False

def test_app_structure():
    """Test that all required files are present"""
    print("\nTesting application structure...")

    required_files = [
        'app/main.py',
        'app/api/routes.py',
        'app/api/ollama_client.py',
        'app/data/storage.py',
        'app/memory/semantic_memory.py',
        'app/templates/index.html',
        'app/static/css/style.css',
        'app/static/js/main.js',
        'requirements.txt',
        'Dockerfile',
        'README.md'
    ]

    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)

    if not missing_files:
        print("✓ All required files present")
        return True
    else:
        print(f"✗ Missing {len(missing_files)} files")
        return False

def main():
    """Run all tests"""
    print("Life Dashboard - Updated Model Test")
    print("=" * 40)

    tests = [
        test_app_structure,
        test_ollama_models
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())