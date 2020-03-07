import asyncio
import datetime
from typing import Optional

from pyppeteer import launch
from pyppeteer.browser import Browser, BrowserContext
from pyppeteer.element_handle import ElementHandle
from pyppeteer.input import Keyboard
from pyppeteer.page import Page

import tools
from config import system


class BaseDominator:

    def __init__(self):
        self.browser = Browser
        self.context = BrowserContext
        self.page = Page
        self.main_page = Page

    async def __aenter__(self):
        self.browser = await launch(headless=False,  # headless=bool(1 - config.debug),
                                    devtools=True,
                                    userDataDir=system.userDataDir,
                                    args=['--disable-infobars', '--no-sandbox'])
        self.context = self.browser
        # self.context = await self.browser.createIncognitoBrowserContext()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if not self.page.isClosed():
            await self.page.close()
        await self.context.close()
        await self.browser.close()

    async def new_page(self) -> Page:
        page = await self.context.newPage()
        await page.setUserAgent(system.ua)
        await page.setViewport({'width': system.width, 'height': system.height, 'isMobile': True, 'hasTouch': True})
        return page

    async def goto(self, target: str, timeout=3000):
        # if type(self.page.url) is not str:
        print('open page')
        self.page = await self.new_page()
        # noinspection PyBroadException
        try:
            await self.page.goto(target, options={'timeout': timeout})
        except Exception:
            pass

        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

    async def reload(self):
        await self.page.reload()

    async def move(self, x, y):
        js = 'window.scroll({0}, {1});'.format(x, y)
        await self.page.evaluate(pageFunction=js)

    async def switch(self):
        await self.main_page.evaluate(pageFunction='window.scrollBy(0, window.innerHeight)')
        await self.main_page.bringToFront()
        await self.main_page.reload()
        await asyncio.sleep(2)
        await self.page.bringToFront()

    async def fetch(self, xpath, timeout=1000) -> bool:
        # noinspection PyBroadException
        try:
            await self.page.waitForXPath(xpath, options={'visible': True, 'timeout': timeout, 'isMobile': True})
        except Exception:
            return False
        return True

    async def get(self, xpath) -> Optional[ElementHandle]:
        items = await self.page.xpath(xpath)
        if items:
            return items[0]
        else:
            return None

    async def wait(self, xpath, timeout=1000) -> bool:
        # noinspection PyBroadException
        try:
            await self.page.waitForXPath(xpath, options={'timeout': timeout})
        except Exception:
            return False
        return True

    async def check(self, xpath, timeout=100) -> bool:
        # noinspection PyBroadException
        try:
            await self.page.waitForXPath(xpath, options={'visible': True, 'timeout': timeout})
        except Exception:
            return False
        return True

    async def type_input(self, xpath, val):
        item = await self.get(xpath)
        if item:
            result = await item.getProperty('value')
            value = await result.jsonValue()
            if value != val:
                await item.type(val)

    async def click(self, xpath):
        item = await self.get(xpath)
        if item:
            await item.click()

    # 时间是否过期
    def is_expired(self, putaway_time) -> bool:
        now = datetime.datetime.now()
        return (now - putaway_time).seconds > 3

    async def is_sold_out(self) -> bool:
        pass

    async def is_login(self) -> bool:
        pass

    async def login(self):
        pass

    # 等待上架
    async def wait_putaway(self):
        wait_time = tools.get_wait()
        print('等待商品上架 ---- 剩余{0}秒'.format(wait_time))
        await asyncio.sleep(wait_time - 0.5)

    async def has_remain(self):
        pass

    async def choose(self):
        pass

    async def amount(self):
        pass

    async def order(self):
        pass

    async def buy(self):
        pass
