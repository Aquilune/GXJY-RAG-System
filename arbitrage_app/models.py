from django.db import models
import datetime
from WindPy import w

w.start()

w.isconnected()  # 判断WindPy是否已经登录成功

# w.menu()
#
# print(w.wsq("IF2504.CFE","rt_settle,rt_est_settle"))
#
# user_input = input("请输入任意内容，然后按回车键继续：")



# 这个模型类用于在数据库中存储套利相关的数据
class ArbitrageData(models.Model):
    ##################
    ##  实时数据部分  ##
    ##################
    # 近月合约的价格，使用 FloatField 来存储浮点数类型的数据
    near_month_price = models.FloatField()
    # 远月合约的价格，同样使用 FloatField 存储浮点数
    far_month_price = models.FloatField()

    ##################
    ##  固定数据部分  ##
    ##################
    # 仓储费用，FloatField 存储浮点数
    storage_fee = models.FloatField()
    # 交易手续费，FloatField 存储浮点数
    trading_fee = models.FloatField()
    # 交割手续费，FloatField 存储浮点数
    delivery_fee = models.FloatField()
    # 资金费用，FloatField 存储浮点数
    capital_cost = models.FloatField()
    # 税值，FloatField 存储浮点数
    tax = models.FloatField()
    # 增值税，FloatField 存储浮点数
    vat = models.FloatField()
    # 印花税，FloatField 存储浮点数
    stamp_duty = models.FloatField()
    # 成本税，FloatField 存储浮点数
    cost_tax = models.FloatField()

    ##################
    ##  计算数据部分  ##
    ##################
    # 价差 = 远月价格 - 近月价格
    # null=True 表示数据库中该字段可以为 NULL
    # blank=True 表示在表单验证时该字段可以为空
    price_spread = models.FloatField(null=True, blank=True)
    # 套利成本 = 仓储费用 + 交易手续费 + 交割手续费 + 资金费用 + 税值
    arbitrage_cost = models.FloatField(null=True, blank=True)
    # 净差价 = 价差 - 套利成本
    net_spread = models.FloatField(null=True, blank=True)
    # 年收益率，根据净差价和近月价格以及跨期时间计算得出 净差价/近月价格/跨期时间*360
    annual_return = models.FloatField(null=True, blank=True)

    ##################
    ##  日期时间部分  ##
    ##################
    # 交割日期，使用 DateField 存储日期类型的数据
    delivery_date = models.DateField()
    # 跨期时间，以整数形式存储，单位可能是天
    inter_period_time = models.IntegerField()

    # 重写 save 方法，在保存数据到数据库之前进行套利相关的计算
    def save(self, near_code, far_code, *args, **kwargs):
        if near_code and far_code and w.isconnected():
            # 获取近月合约价格
            self.near_month_price = w.wsq(near_code, "rt_latest").Data[0][0]
            # 获取远月合约价格
            self.far_month_price = w.wsq(far_code, "rt_latest").Data[0][0]

            # 计算价差，公式为：价差 = 远月价格 - 近月价格
            self.price_spread = self.far_month_price - self.near_month_price
            # 计算税值，公式为：税值 = 增值税 + 印花税 - 成本税
            self.tax = self.vat + self.stamp_duty - self.cost_tax
            # 计算套利成本，公式为：套利成本 = 仓储费用 + 交易手续费 + 交割手续费 + 资金费用 + 税值
            self.arbitrage_cost = self.storage_fee + self.trading_fee + self.delivery_fee + self.capital_cost + self.tax
            # 计算净差价，公式为：净差价 = 价差 - 套利成本
            self.net_spread = self.price_spread - self.arbitrage_cost
            # 计算年收益率，公式为：年收益率 = ( 净差价 / 近月价格 / 跨期时间 ) * 360 (跨期时间暂定为60)
            self.annual_return = (self.net_spread / self.near_month_price / self.inter_period_time) * 360

            # 调用父类的 save 方法，将数据保存到数据库中
            super().save(*args, **kwargs)
        else:
            print("WindPy 连接失败，请检查网络或授权。")

