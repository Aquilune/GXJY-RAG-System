
# 定义所有数据提供商的抽象接口
class BaseDataProvider(object):
    def __init__(self):
        pass

    def get_near_month_price(self, near_code):
        raise NotImplementedError("无法获取近月合约")

    def get_far_month_price(self, far_code):
        raise NotImplementedError("无法获取远月合约")