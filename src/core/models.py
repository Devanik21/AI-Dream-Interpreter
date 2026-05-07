"""
Data models for dream journal entries.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DreamEntry:
    text: str
    date: str
    emotions: List[str]
    lucidity: int
