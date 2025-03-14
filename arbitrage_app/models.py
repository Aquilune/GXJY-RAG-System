from django.db import models

from arbitrage_app.data_providers import get_data_provider


# 这个模型类用于在数据库中存储套利相关的数据
class ArbitrageData(models.Model):
    """
      实时数据部分
    """
    near_month_code = models.CharField(max_length=50)  # 近月合约的代码
    far_month_code = models.CharField(max_length=50) # 远月合约的代码
    near_month_price = models.FloatField()  # 近月合约的价格
    far_month_price = models.FloatField()  # 远月合约的价格

    """
      固定数据部分
    """

    trading_fee = models.FloatField()  # 交易手续费
    delivery_fee = models.FloatField()  # 交割手续费
    capital_cost = models.FloatField()  # 资金费用
    vat = models.FloatField()  # 增值税

    """
      日期数据部分
    """

    first_delivery_date = models.DateField()  # 第一合约交割日期
    second_delivery_date = models.DateField()  # 第二合约交割日期

    """
      计算数据部分
    """
    inter_period_time = models.IntegerField()  # 跨期时间 = 第二合约交割日期 - 第一合约交割日期
    storage_fee = models.FloatField()  # 仓储费用 = 0.5 * 跨期时间
    stamp_duty = models.FloatField()  # 印花税 = (近月价格+远月价格)*0.0003
    cost_tax = models.FloatField()  # 成本税 = (仓储费用+交易手续费+交割手续费)/1.06*0.06
    tax = models.FloatField()  # 税值 = 增值税+印花税-成本税
    price_spread = models.FloatField(null=True, blank=True)  # 价差 = 远月价格 - 近月价格
    arbitrage_cost = models.FloatField(null=True, blank=True)  # 套利成本 = 仓储费用 + 交易手续费 + 交割手续费 + 资金费用 + 税值
    net_spread = models.FloatField(null=True, blank=True)  # 净差价 = 价差 - 套利成本
    annual_return = models.FloatField(null=True, blank=True)  # 年收益率，根据净差价和近月价格以及跨期时间计算得出 净差价/近月价格/跨期时间*360

    # 重写 save 方法，在保存数据到数据库之前进行套利相关的计算
    def save(self, *args, **kwargs):
        if self.near_month_code and self.far_month_code:

            provider = get_data_provider()
            self.near_month_price = provider.get_near_month_price(self.near_month_code)
            self.far_month_price = provider.get_near_month_price(self.far_month_code)
            self.inter_period_time = self.second_delivery_date - self.first_delivery_date
            self.storage_fee = 0.5 * self.inter_period_time
            self.stamp_duty = ( self.near_month_price + self.far_month_price ) * 0.0003
            self.price_spread = self.far_month_price - self.near_month_price  # 计算价差，公式为：价差 = 远月价格 - 近月价格
            self.cost_tax = (self.storage_fee + self.trading_fee + self.delivery_fee)/1.06 * 0.06
            self.tax = self.vat + self.stamp_duty - self.cost_tax  # 计算税值，公式为：税值 = 增值税 + 印花税 - 成本税
            self.arbitrage_cost = self.storage_fee + self.trading_fee + self.delivery_fee + self.capital_cost + self.tax  # 计算套利成本，公式为：套利成本 = 仓储费用 + 交易手续费 + 交割手续费 + 资金费用 + 税值
            self.net_spread = self.price_spread - self.arbitrage_cost  # 计算净差价，公式为：净差价 = 价差 - 套利成本
            self.annual_return = (self.net_spread / self.near_month_price / self.inter_period_time) * 360  # 计算年收益率，公式为：年收益率 = ( 净差价 / 近月价格 / 跨期时间 ) * 360 (跨期时间暂定为60)
            # 调用父类的 save 方法，将数据保存到数据库中
            super().save(*args, **kwargs)
        else:
            print("WindPy 连接失败，请检查网络或授权。")
