#!/usr/bin/env python3
"""
Test script to verify memory functionality works correctly
"""

import os
import sys
import json

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_memory_add():
    """Test that we can add and retrieve memory entries"""
    print("Testing memory functionality...")

    try:
        from app.memory.semantic_memory import add_to_memory, get_memory

        # Add a test memory entry
        test_memory = "This is a test memory entry for the Life Dashboard"
        add_to_memory(test_memory)

        # Retrieve memory
        memory = get_memory()

        if len(memory) > 0:
            print("✓ Memory entry added and retrieved successfully")
            print(f"  Found {len(memory)} memory entries")
            return True
        else:
            print("✗ No memory entries found")
            return False

    except Exception as e:
        print(f"✗ Error testing memory functionality: {e}")
        return False

def test_ollama_summary():
    """Test that the week summary function works"""
    print("\nTesting Ollama summary functionality...")

    try:
        from app.api.ollama_client import summarize_week

        # Test the summarize_week function
        summary = summarize_week()
        print("✓ Week summary function executed")
        print(f"  Summary: {summary[:100]}...")
        return True

    except Exception as e:
        print(f"✗ Error testing Ollama summary: {e}")
        return False

def main():
    """Run all tests"""
    print("Life Dashboard - Memory Functionality Test")
    print("=" * 50)

    tests = [
        test_memory_add,
        test_ollama_summary
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("✓ All memory functionality tests passed!")
        return 0
    else:
        print("✗ Some memory functionality tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())