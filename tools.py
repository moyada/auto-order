import asyncio
import datetime

from config import system, order


def get_wait() -> int:
    if system.debug:
        return 3
    t1 = datetime.datetime.now()
    t2 = datetime.datetime.strptime(order.time, "%Y-%m-%d %H:%M:%S")
    wait_time = (t2 - t1).seconds
    return wait_time


def sync_run(func):
    asyncio.get_event_loop().run_until_complete(func)


def sync_call(future):
    return asyncio.ensure_future(future)
