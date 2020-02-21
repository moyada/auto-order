import asyncio
import datetime

import config
import url


def get_wait() -> int:
    if config.debug:
        return 3
    t1 = datetime.datetime.now()
    t2 = datetime.datetime.strptime(config.time, "%Y-%m-%d %H:%M:%S")
    wait_time = (t2 - t1).seconds
    return wait_time


def sync_run(func):
    asyncio.get_event_loop().run_until_complete(func)


def sync_call(future):
    return asyncio.ensure_future(future)


def is_main_page(s: str):
    return s.startswith(url.login)


if __name__ == '__main__':
    print(bool(1 - True))
    print(bool(1 - False))