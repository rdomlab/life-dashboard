#!/usr/bin/env python3
"""
Initialize the Life Dashboard database with sample data
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def main():
    """Initialize the database with sample data"""
    print("Initializing Life Dashboard database with sample data...")

    try:
        from app.data.storage import seed_database

        # Seed the database
        seed_database()
        print("✓ Database initialized with sample data")

    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()