username = "xxx"
password = "xxxxxxx"

userDataDir = '/tmp/taobaoData'
scan_time = 20

# sku = "https://detail.tmall.com/item.htm?id=612000633944"
sku = "https://detail.tmall.com/item.htm?id=612483226819"
is_tmall = sku.count('tmall') > 0

time = "2020-02-20 14:01:00"
amount = 1

taobao_amount = '//*[@id="J_IptAmount"]'
tmall_amount = '//*[@id="J_Amount"]/span[1]/input'
taobao_order = '//*[@id="J_juValid"]/div[1]/a'
tmall_order = '//*[@id="J_LinkBuy"]'
taobao_check = '//*[@id="J_juValid"]/div[1]/a'
tmall_check = '//*[@id="J_LinkBuy"]'

width = 1366
height = 768
debug = False
