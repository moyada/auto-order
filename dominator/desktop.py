import datetime

from config import user, order, system
from dominator._base import BaseDominator


class PlatformDominator(BaseDominator):

    async def is_login(self) -> bool:
        return False

    async def login(self):
        await self.goto(target=system.desktop_login_url, timeout=5000)
        if await self.fetch('//*[@id="J_LoginBox"]/div[1]/div[1]', timeout=3000):
            await self.click('//*[@id="J_LoginBox"]/div[1]/div[1]')
        await self.type_input('//*[@id="TPL_username_1"]', user.username)
        await self.type_input('//*[@id="TPL_password_1"]', user.password)
        await self.click('//*[@id="J_SubmitStatic"]')

    async def is_sold_out(self) -> bool:
        sold_out = await self.fetch('//*[@id="J_Sold-out-recommend"]/div[1]/div[1]/strong', 0)
        return sold_out

    async def buy(self):
        await self.fetch('//*[@id="submitOrderPC_1"]/div[1]/a', timeout=3000)
        await self.click('//*[@id="submitOrderPC_1"]/div[1]/a')


class Tmall(PlatformDominator):

    async def has_remain(self) -> bool:
        putaway_time = datetime.datetime.strptime(order.time, "%Y-%m-%d %H:%M:%S")

        # 倒计时页面，等到倒记时结束即可直接购买
        if not await self.check('//*[@id="J_LinkBuy"]'):
            now = datetime.datetime.now()
            return await self.wait('//*[@id="J_LinkBuy"]', (now - putaway_time).seconds * 1000)

        # 商品下架中
        while True:
            # noinspection PyBroadException
            try:
                await self.page.reload(options={'timeout': 1000})
            except Exception:
                pass
            print('reload')
            if not self.is_sold_out():
                return True
            if self.is_expired(putaway_time):
                return False

    async def amount(self):
        if order.amount == 1:
            return
        amount = await self.get('//*[@id="J_Amount"]/span[1]/input')
        await amount.press('Delete')
        await amount.type(str(order.amount))

    async def order(self):
        await self.click('//*[@id="J_LinkBuy"]')


class Taobao(PlatformDominator):

    async def has_remain(self) -> bool:
        putaway_time = datetime.datetime.strptime(order.time, "%Y-%m-%d %H:%M:%S")

        # 倒计时页面，等到倒记时结束即可直接购买
        if not await self.check('//*[@id="J_juValid"]/div[1]/a'):
            now = datetime.datetime.now()
            return await self.wait('//*[@id="J_juValid"]/div[1]/a', (now - putaway_time).seconds * 1000)

        # 商品下架中
        while True:
            # noinspection PyBroadException
            try:
                await self.page.reload(options={'timeout': 1000})
            except Exception:
                pass
            print('reload')
            if not self.is_sold_out():
                return True
            if self.is_expired(putaway_time):
                return False

    async def amount(self):
        if order.amount == 1:
            return
        amount = await self.get('//*[@id="J_IptAmount"]')
        await amount.press('Delete')
        await amount.type(str(order.amount))

    async def order(self):
        await self.click('//*[@id="J_juValid"]/div[1]/a')
