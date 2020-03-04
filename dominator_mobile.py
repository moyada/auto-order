import asyncio
import datetime
from typing import Optional

from pyppeteer import launch
from pyppeteer.browser import Browser, BrowserContext
from pyppeteer.element_handle import ElementHandle
from pyppeteer.page import Page

import config
import tools


browser = Browser
context = BrowserContext
page = Page


async def init():
    global browser, context
    browser = await launch(headless=False,
                           # headless=bool(1 - config.debug),
                           userDataDir=config.userDataDir,
                           args=['--disable-infobars'])
    context = await browser.createIncognitoBrowserContext()


async def goto(target: str, timeout=3000):
    global page
    # if page.url is str:
    #     await page.close()
    page = await context.newPage()
    await page.setViewport({'width': config.width, 'height': config.height})

    # noinspection PyBroadException
    try:
        await page.goto(target, options={'timeout': timeout})
    except Exception:
        pass

    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')


async def login():
    await type_input('//*[@id="username"]', config.username)
    await type_input('//*[@id="password"]', config.password)
    await click('//*[@id="btn-submit"]')
    print('登陆账号')


async def get(xpath) -> Optional[ElementHandle]:
    # noinspection PyBroadException
    try:
        elems = await page.xpath(xpath)
    except Exception:
        return None
    return elems[0]


async def fetch(xpath, timeout=1000) -> bool:
    # noinspection PyBroadException
    try:
        await page.waitForXPath(xpath, options={'timeout': timeout})
    except Exception:
        return False
    return True


async def check(xpath, timeout=100) -> bool:
    # noinspection PyBroadException
    try:
        await page.waitForXPath(xpath, options={'visible': True, 'timeout': timeout})
    except Exception:
        return False
    return True


async def wait(xpath, sleep_time) -> bool:
    await asyncio.sleep(sleep_time)
    return await check(xpath)


async def type_input(xpath, val):
    items = await page.xpath(xpath)
    if items:
        result = await items[0].getProperty('value')
        value = await result.jsonValue()
        if value != config.username:
            await items[0].type(val)


async def click(xpath):
    items = await page.xpath(xpath)
    if items:
        await items[0].click()


# 等待上架
async def wait_putaway():
    wait_time = tools.get_wait()
    print('等待商品上架 ---- 剩余{0}秒'.format(wait_time))
    await asyncio.sleep(wait_time - 0.5)


# 时间是否过期
def is_expired(putaway_time) -> bool:
    now = datetime.datetime.now()
    return (now - putaway_time).seconds > 3


async def is_sold_out() -> bool:
    sold_out = await fetch('//*[@id="J_Sold-out-recommend"]/div[1]/div[1]/strong', 0)
    return sold_out


# 是否有库存
async def has_remain() -> bool:
    print('开始抢购')
    putaway_time = datetime.datetime.strptime(config.time, "%Y-%m-%d %H:%M:%S")

    # 倒计时页面，等到倒记时结束即可直接购买
    if config.is_tmall:
        if not await check(config.tmall_check):
            now = datetime.datetime.now()
            return await wait(config.tmall_order, (now - putaway_time).seconds * 1000)
    else:
        if not await check(config.taobao_check):
            now = datetime.datetime.now()
            return await wait(config.taobao_order, (now - putaway_time).seconds * 1000)

    # 商品下架中
    while True:
        # noinspection PyBroadException
        try:
            await page.reload(options={'timeout': 1000})
        except Exception:
            pass
        print('reload')
        if not is_sold_out():
            return True
        if is_expired(putaway_time):
            return False


# 选择类型
async def choose():
    group = await page.xpath('//*[@id="J_relateGroup"]/dd/ul/li[2]/a')
    sku = await page.xpath('//*[@id="J_isku"]/div/dl[1]/dd/ul/li/a')
    item = await page.xpath('//*[@id="J_isku"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[3]/a')


# 选择数量
async def amount():
    if config.amount == 1:
        return

    if config.is_tmall:
        amounts = await page.xpath(config.tmall_amount)
    else:
        amounts = await page.xpath(config.taobao_amount)

    await amounts[0].press('Delete')
    await amounts[0].type(str(config.amount))


# 下单
async def order():
    if config.is_tmall:
        await click(config.tmall_order)
    else:
        await click(config.taobao_order)
    print('下单')


# 购买
async def buy():
    await fetch('//*[@id="submitOrderPC_1"]/div[1]/a', timeout=3000)
    await click('//*[@id="submitOrderPC_1"]/div[1]/a')
    print('抢购成功!!')


async def close():
    if not page.isClosed():
        await page.close()
    await context.close()
    await browser.close()