from collections import deque
from time import time

class RecentEventBuffer:
    """Keeps events from the last `window_seconds`, dropping older ones automatically."""

    def __init__(self, window_seconds=300):  # 300s = 5 minutes, tune as needed
        self.window_seconds = window_seconds
        self._buffer = deque()

    def add(self, data: dict):
        self._buffer.append({"t": time(), **data})
        self._expire_old()

    def _expire_old(self):
        cutoff = time() - self.window_seconds
        while self._buffer and self._buffer[0]["t"] < cutoff:
            self._buffer.popleft()

    def get_all(self):
        """Call this to read current buffer contents (e.g. for frontend/API)."""
        self._expire_old()
        return list(self._buffer)

    def clear(self):
        self._buffer.clear()