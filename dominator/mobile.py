import asyncio

from config import user, system
from dominator._base import BaseDominator


class PlatformDominator(BaseDominator):

    async def is_login(self) -> bool:
        await self.goto(target=system.mobile_main_url, timeout=5000)
        await asyncio.sleep(3)
        return not await self.fetch('/html/body/div[2]/div')

    async def login(self):
        await self.goto(target=system.mobile_login_url, timeout=5000)
        await self.type_input('//*[@id="username"]', user.username)
        await self.type_input('//*[@id="password"]', user.password)
        await self.click('//*[@id="btn-submit"]')
        await asyncio.sleep(2)
        self.main_page = self.page

    async def is_sold_out(self) -> bool:
        pass


class Tmall(PlatformDominator):

    async def has_remain(self) -> bool:
        return await self.check('//*[@id="s-actionBar-container"]/div/div[2]/a[3]')

    async def amount(self):
        pass

    async def order(self):
        await self.fetch('//*[@id="s-actionBar-container"]/div/div[2]/a[3]', timeout=3000)
        await self.click('//*[@id="s-actionBar-container"]/div/div[2]/a[3]')
        await self.fetch('/html/body/div[5]/div[2]/div/div[3]/a', timeout=1000)
        await self.click('/html/body/div[5]/div[2]/div/div[3]/a')

    async def buy(self):
        await self.fetch('//*[@id="submitBlock_1"]/div/div/div/div[3]/div[2]/span', timeout=3000)
        await self.click('//*[@id="submitBlock_1"]/div/div/div/div[3]/div[2]/span')


class Taobao(PlatformDominator):

    async def has_remain(self) -> bool:
        return await self.check('//*[@id="detailInfoContainer"]/div[4]/div[5]')

    async def amount(self):
        pass

    async def order(self):
        await self.fetch('//*[@id="detailInfoContainer"]/div[4]/div[5]', timeout=3000)
        await self.click('//*[@id="detailInfoContainer"]/div[4]/div[5]')

    async def buy(self):
        await self.fetch('//*[@id="submitOrder_1"]/div[2]/div[2]', timeout=3000)
        await self.click('//*[@id="submitOrder_1"]/div[2]/div[2]')
