from django.db import models

from arbitrage_app.data_providers import get_data_provider


from django.db import models
from datetime import timedelta

class ArbitrageData(models.Model):
    """
      实时数据部分
    """
    near_month_code = models.CharField(max_length=50)  # 近月合约代码
    far_month_code = models.CharField(max_length=50)  # 远月合约代码
    near_month_price = models.FloatField()  # 近月合约价格
    far_month_price = models.FloatField()  # 远月合约价格

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
    inter_period_time = models.IntegerField()  # 跨期时间（天数）
    storage_fee = models.FloatField()  # 仓储费用 = 0.5 * 跨期时间
    stamp_duty = models.FloatField()  # 印花税 = (近月价格+远月价格) * 0.0003
    cost_tax = models.FloatField()  # 成本税 = (仓储费用+交易手续费+交割手续费) / 1.06 * 0.06
    tax = models.FloatField()  # 税值 = 增值税 + 印花税 - 成本税
    price_spread = models.FloatField(null=True, blank=True)  # 价差 = 远月价格 - 近月价格
    arbitrage_cost = models.FloatField(null=True, blank=True)  # 套利成本 = 仓储费用 + 交易手续费 + 交割手续费 + 资金费用 + 税值
    net_spread = models.FloatField(null=True, blank=True)  # 净差价 = 价差 - 套利成本
    annual_return = models.FloatField(null=True, blank=True)  # 年收益率 = 净差价 / 近月价格 / 跨期时间 * 360

    def save(self, *args, **kwargs):
        if not self.near_month_code or not self.far_month_code:
            raise ValueError("请输入有效的合约代码")

        # 确保交割日期正确
        if self.first_delivery_date >= self.second_delivery_date:
            raise ValueError("第一合约交割日期必须早于第二合约交割日期")

        # 计算跨期时间
        days = (self.second_delivery_date - self.first_delivery_date).days
        if days <= 0:
            raise ValueError("跨期时间必须大于0")

        self.inter_period_time = days

        # 获取最新市场价格
        # provider = get_data_provider()
        # self.near_month_price = provider.get_near_month_price(self.near_month_code)
        # self.far_month_price = provider.get_near_month_price(self.far_month_code)
        self.near_month_price = 24.6
        self.far_month_price = 23.6

        # 计算仓储费用
        self.storage_fee = 0.5 * days

        # 计算印花税
        self.stamp_duty = (self.near_month_price + self.far_month_price) * 0.0003

        # 计算价差
        self.price_spread = self.far_month_price - self.near_month_price

        # 计算成本税
        self.cost_tax = (self.storage_fee + self.trading_fee + self.delivery_fee) / 1.06 * 0.06

        # 计算税值
        self.tax = self.vat + self.stamp_duty - self.cost_tax

        # 计算套利成本
        self.arbitrage_cost = self.storage_fee + self.trading_fee + self.delivery_fee + self.capital_cost + self.tax

        # 计算净差价
        self.net_spread = self.price_spread - self.arbitrage_cost

        # 计算年收益率
        self.annual_return = (self.net_spread / self.near_month_price / days) * 360 if days > 0 else 0

        super().save(*args, **kwargs)  # 确保调用父类 `save` 方法存入数据库
