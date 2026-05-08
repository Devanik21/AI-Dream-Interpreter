"""
Data models for dream journal entries.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class DreamEntry:
    text: str
    date: datetime
    emotions: List[str]
    lucidity: int
