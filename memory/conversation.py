"""
Memory — Manages conversation history across turns.
Without this, the agent forgets the previous question every time.
"""

from typing import List, Dict
from utils.logger import get_logger

logger = get_logger("memory.conversation")


class ConversationMemory:
    def __init__(self, max_turns: int = 20):
        self.history: List[Dict[str, str]] = []
        self.max_turns = max_turns

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "parts": [message]})
        self._trim()
        logger.debug(f"User message added. History length: {len(self.history)}")

    def add_assistant_message(self, message: str):
        self.history.append({"role": "model", "parts": [message]})
        logger.debug(f"Assistant message added. History length: {len(self.history)}")

    def get_history(self) -> List[Dict]:
        return self.history

    def clear(self):
        self.history = []
        logger.info("Conversation memory cleared")

    def _trim(self):
        """Keep only the last N turns to avoid context overflow."""
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]
            logger.warning("History trimmed to stay within context limits")
