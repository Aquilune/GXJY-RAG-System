from django.test import TestCase
from .models import ArbitrageData
from WindPy import w
import datetime

# 初始化 WindPy
w.start()

class ArbitrageDataTestCase(TestCase):
    def setUp(self):
        # 在每个测试方法执行前，创建一个 ArbitrageData 实例并设置必要的属性
        self.arbitrage = ArbitrageData(
            latest_price = 100,
            storage_fee=100,
            trading_fee=50,
            delivery_fee=20,
            capital_cost=30,
            vat=15,
            stamp_duty=5,
            cost_tax=10,
            delivery_date=datetime.date.today(),
            inter_period_time=90
        )

    def test_save_function(self):
        # 动态指定合约代码
        near_code = "IF2504.CFE"
        far_code = "IF2503.CFE"

        # 调用 save 方法
        self.arbitrage.save(near_code, far_code)

        # # 检查计算结果是否正确
        # price_spread = self.arbitrage.far_month_price - self.arbitrage.near_month_price
        # arbitrage_cost = (
        #     self.arbitrage.storage_fee +
        #     self.arbitrage.trading_fee +
        #     self.arbitrage.delivery_fee +
        #     self.arbitrage.capital_cost +
        #     self.arbitrage.vat +
        #     self.arbitrage.stamp_duty +
        #     self.arbitrage.cost_tax
        # )
        # net_spread = price_spread - arbitrage_cost
        # annual_return = (net_spread / self.arbitrage.near_month_price) * (365 / self.arbitrage.inter_period_time)
        #
        # self.assertEqual(self.arbitrage.price_spread, price_spread)
        # self.assertEqual(self.arbitrage.arbitrage_cost, arbitrage_cost)
        # self.assertEqual(self.arbitrage.net_spread, net_spread)
        # self.assertEqual(self.arbitrage.annual_return, annual_return)