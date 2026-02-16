import json
import os
from typing import Any, Dict, List, Optional
from src.memory.base_memory import BaseMemory

class LocalMemory(BaseMemory):
    \"\"\"
    A persistent local file-based memory implementation.
    Stores memories in a JSON file for simplicity and reliability.
    \"\"\"

    def __init__(self, storage_path: str = \"data/memory.json\"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
        self.memories: List[Dict[str, Any]] = self._load_memories()

    def _ensure_storage_exists(self) -> None:
        \"\"\"Create the data directory and memory file if they don't exist.\"\"\"
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, \"w\", encoding=\"utf-8\") as f:
                json.dump([], f)

    def _load_memories(self) -> List[Dict[str, Any]]:
        \"\"\"Load memories from the local JSON file.\"\"\"
        try:
            with open(self.storage_path, \"r\", encoding=\"utf-8\") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_memories(self) -> None:
        \"\"\"Save the current memory state to the local JSON file.\"\"\"
        with open(self.storage_path, \"w\", encoding=\"utf-8\") as f:
            json.dump(self.memories, f, indent=4)

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        \"\"\"Add a memory entry with a timestamp and persistent save.\"\"\"
        entry = {
            \"timestamp\": self._format_timestamp(),
            \"content\": content,
            \"metadata\": metadata or {}
        }
        self.memories.append(entry)
        self._save_memories()

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        \"\"\"
        Simple keyword-based search for memories.
        In a production environment, this would be replaced by vector similarity search.
        \"\"\"
        results = [
            m for m in self.memories 
            if query.lower() in m[\"content\"].lower()
        ]
        return results[:limit]

    def clear(self) -> None:
        \"\"\"Clear all memories and reset the file.\"\"\"
        self.memories = []
        self._save_memories()

    def get_all(self) -> List[Dict[str, Any]]:
        \"\"\"Retrieve the complete memory history.\"\"\"
        return self.memories
