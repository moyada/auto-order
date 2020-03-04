username = "xxx"
password = "xxxxxxx"

userDataDir = '/tmp/taobaoData'
scan_time = 20

sku = "https://detail.m.tmall.com/item.htm?id=528351172546"
# sku = "https://h5.m.taobao.com/awp/core/detail.html?id=574329781541"
is_tmall = sku.count('tmall') > 0

time = "2020-02-23 20:05:00"
amount = 5

taobao_amount = '//*[@id="J_IptAmount"]'
tmall_amount = '//*[@id="J_Amount"]/span[1]/input'
taobao_order = '//*[@id="J_juValid"]/div[1]/a'
taobao_order_m = '//*[@id="detailInfoContainer"]/div[4]/div[5]'
tmall_order_m = '//*[@id="s-actionBar-container"]/div/div[2]/a[3]'
tmall_confirm_m = '/html/body/div[3]/div[2]/div/div[3]/a'
tmall_order = '//*[@id="J_LinkBuy"]'
taobao_check = '//*[@id="J_juValid"]/div[1]/a'
tmall_check = '//*[@id="J_LinkBuy"]'

submit_m = '//*[@id="submitOrder_1"]/div[2]/div[2]/div'


width = 730
height = 1280
debug = True
