"""Bounded FIFO admission queue for CPU-heavy jobs (STL generation).

At most `concurrency` jobs run at once; the rest wait their turn in arrival order instead of
being rejected. The queue itself is bounded (total and per client) and waiting is capped, so a
burst or a single abusive client cannot make legitimate requests pile up forever.
"""
import asyncio
from collections import Counter
from contextlib import asynccontextmanager


class QueueFull(Exception):
    """No room left in the queue: the caller should retry later."""


class QueueTimeout(Exception):
    """The job waited too long for a free slot."""


class JobQueue:
    def __init__(self, concurrency: int = 2, max_waiting: int = 20, max_per_client: int = 3, max_wait_seconds: float = 60):
        self._slots = asyncio.Semaphore(concurrency)  # asyncio.Semaphore wakes waiters in FIFO order
        self._max_waiting = max_waiting
        self._max_per_client = max_per_client
        self._max_wait = max_wait_seconds
        self._waiting = 0
        self._per_client = Counter()

    @property
    def waiting(self) -> int:
        return self._waiting

    @asynccontextmanager
    async def slot(self, client: str):
        if self._waiting >= self._max_waiting or self._per_client[client] >= self._max_per_client:
            raise QueueFull()

        self._waiting += 1
        self._per_client[client] += 1
        try:
            await asyncio.wait_for(self._slots.acquire(), timeout=self._max_wait)
        except asyncio.TimeoutError:
            raise QueueTimeout() from None
        finally:
            # Also runs when the client disconnects (task cancelled), freeing its place in line.
            self._waiting -= 1
            self._per_client[client] -= 1
            if not self._per_client[client]:
                del self._per_client[client]

        try:
            yield
        finally:
            self._slots.release()
