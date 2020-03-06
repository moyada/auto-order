import time
import tools

import asyncio
from pyppeteer import launch

from config import order, system, url
from dominator import desktop, mobile
from dominator._base import BaseDominator


async def test():
    browser = await launch(headless=bool(1 - system.debug),
                           userDataDir=system.userDataDir,
                           args=['--disable-infobars'])
    page = await browser.newPage()
    await page.setViewport({'width': system.width, 'height': system.height})
    await page.goto(url.login)
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await asyncio.sleep(100)
    await browser.close()


def get_dominator() -> BaseDominator:
    sku_url = order.sku
    if sku_url.count(system.tmall_prefix):
        return desktop.Tmall()

    if sku_url.count(system.taobao_prefix):
        return desktop.Taobao()

    if sku_url.count(system.tmall_m_prefix):
        return mobile.Tmall()

    if sku_url.count(system.taobao_m_prefix):
        return mobile.Taobao()

    raise Exception('invalid sku url: {}'.format(sku_url))


# @asyncio.coroutine
async def main():
    async with get_dominator() as dominate:
        await dominate.login()
        # await dominate.move(0, 100)
        print('登陆账号')
        await asyncio.sleep(2)
        await dominate.goto(order.sku)
        await dominate.wait_putaway()

        print('开始抢购')
        has_remain = await dominate.has_remain()
        if has_remain:
            # await dominator.choose()
            await dominate.amount()
            await dominate.order()
            await dominate.buy()
            print('抢购成功!!')
        else:
            print('抢购失败')

        await asyncio.sleep(2)
        await dominate.goto(order.sku)
        await asyncio.sleep(30000)

# https://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p03_parsing_command_line_options.html
# https://juejin.im/post/5c6958fd6fb9a049ff4eab60

if __name__ == '__main__':
    wait_time = tools.get_wait()
    if wait_time > 60:
        print('等待抢购开始 ---- 剩余{0}秒'.format(wait_time - 60))
        time.sleep(wait_time - 60)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
    # loop.run_until_complete(test())

    if loop.is_running():
        loop.close()
