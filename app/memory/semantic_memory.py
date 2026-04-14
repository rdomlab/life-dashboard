import json
import os
import hashlib
from typing import List, Dict, Any
from datetime import datetime

# Memory file
MEMORY_FILE = "app/memory/memory.json"

def init_memory():
    """Initialize semantic memory storage"""
    if not os.path.exists(MEMORY_FILE):
        # Create empty memory file
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"entries": []}, f)

def get_memory() -> List[Dict[str, Any]]:
    """Get all memory entries"""
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
        return data.get("entries", [])
    except Exception:
        return []

def add_to_memory(text: str) -> bool:
    """Add text to semantic memory with timestamp"""
    try:
        # Read existing memory
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)

        # If text is not a string, convert it to JSON
        if not isinstance(text, str):
            text = json.dumps(text, indent=2, ensure_ascii=False)

        # Create new entry
        entry = {
            "id": hashlib.md5(text.encode()).hexdigest(),
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "embedding": generate_embedding(text)  # Simple embedding
        }

        # Add to entries
        data["entries"].append(entry)

        # Write back to file
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error adding to memory: {e}")
        return False

def generate_embedding(text: str) -> List[float]:
    """Generate a simple embedding for text (simplified for demo)"""
    # This is a simplified embedding - in production, you'd use a proper embedding model
    # For now, we'll create a basic hash-based representation
    hash_value = hashlib.md5(text.lower().encode()).hexdigest()
    # Convert hex to list of floats (simplified)
    embedding = [int(hash_value[i:i+2], 16) / 255.0 for i in range(0, len(hash_value), 2)][:10]
    return embedding

def search_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search memory for relevant entries (simplified)"""
    try:
        memory = get_memory()
        # Simple text matching for demo purposes
        results = []
        for entry in memory:
            if query.lower() in entry["text"].lower():
                results.append(entry)
                if len(results) >= limit:
                    break
        return results
    except Exception as e:
        print(f"Error searching memory: {e}")
        return []