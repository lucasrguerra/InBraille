import asyncio

import pytest

from src.web.job_queue import JobQueue, QueueFull, QueueTimeout


async def _run(queue, client, order, name, hold):
    async with queue.slot(client):
        order.append(name)
        await asyncio.sleep(hold)


def test_jobs_run_in_arrival_order_and_none_is_lost():
    async def scenario():
        queue = JobQueue(concurrency=1, max_waiting=10, max_per_client=10)
        order = []
        tasks = []
        for i in range(5):
            tasks.append(asyncio.create_task(_run(queue, f"c{i}", order, i, 0.01)))
            await asyncio.sleep(0)
        await asyncio.gather(*tasks)
        return order, queue.waiting

    order, waiting = asyncio.run(scenario())
    assert order == [0, 1, 2, 3, 4]
    assert waiting == 0


def test_concurrency_is_respected():
    async def scenario():
        queue = JobQueue(concurrency=2, max_waiting=10, max_per_client=10)
        running = peak = 0

        async def job(i):
            nonlocal running, peak
            async with queue.slot(f"c{i}"):
                running += 1
                peak = max(peak, running)
                await asyncio.sleep(0.02)
                running -= 1

        await asyncio.gather(*(job(i) for i in range(6)))
        return peak

    assert asyncio.run(scenario()) == 2


def test_queue_full_and_per_client_cap():
    async def scenario():
        queue = JobQueue(concurrency=1, max_waiting=2, max_per_client=1)
        order = []
        first = asyncio.create_task(_run(queue, "a", order, "a", 0.05))
        await asyncio.sleep(0)
        second = asyncio.create_task(_run(queue, "b", order, "b", 0.0))
        await asyncio.sleep(0)
        with pytest.raises(QueueFull):  # client "b" already holds a place in line
            async with queue.slot("b"):
                pass
        third = asyncio.create_task(_run(queue, "c", order, "c", 0.0))
        await asyncio.sleep(0)
        with pytest.raises(QueueFull):  # the queue itself is full
            async with queue.slot("d"):
                pass
        await asyncio.gather(first, second, third)
        return order

    assert asyncio.run(scenario()) == ["a", "b", "c"]


def test_wait_timeout_and_cancellation_free_the_place():
    async def scenario():
        queue = JobQueue(concurrency=1, max_waiting=5, max_per_client=5, max_wait_seconds=0.05)
        holder = asyncio.create_task(_run(queue, "a", [], "a", 0.3))
        await asyncio.sleep(0)
        with pytest.raises(QueueTimeout):
            async with queue.slot("b"):
                pass
        waiter = asyncio.create_task(_run(queue, "c", [], "c", 0))
        await asyncio.sleep(0.01)
        waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiter
        assert queue.waiting == 0
        await holder

    asyncio.run(scenario())
