import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import apps
import datetime

from arbitrage_app.configurations import *
from arbitrage_app.data_providers import get_data_provider

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 计算价差并给出预警提示
def calculate_spread_and_warn():
    try:
        ArbitrageData = apps.get_model('arbitrage_app', 'ArbitrageData')

        near_code = NEAR_MONTH_CODE_MONITOR
        far_code = FAR_MONTH_CODE_MONITOR

        provider = get_data_provider()

        # 获取近月合约价格
        near_month_data = provider.get_near_month_price(near_code)
        if near_month_data.ErrorCode == 0:
            near_month_price = near_month_data.Data[0][0]
        else:
            logging.error(f"获取近月合约价格失败，错误代码: {near_month_data.ErrorCode}")
            return

        # 获取远月合约价格
        far_month_data = provider.get_far_month_price(far_code)
        if far_month_data.ErrorCode == 0:
            far_month_price = far_month_data.Data[0][0]
        else:
            logging.error(f"获取远月合约价格失败，错误代码: {far_month_data.ErrorCode}")
            return

        spread = far_month_price - near_month_price  # 计算价
        threshold = PRICE_SPREAD_THRESHOLD  # 预设阈值

        if spread > threshold:
            logging.warning(f"价差超过阈值！当前价差: {spread}, 阈值: {threshold}")

        # 保存数据到数据库
        arbitrage_data = ArbitrageData(
            near_month_price=near_month_price,
            far_month_price=far_month_price,
            price_spread=spread,
            delivery_date=datetime.date.today(),
            inter_period_time=60  # 假设跨期时间为 60 天
        )
        arbitrage_data.save()

    except Exception as e:
        logging.error(f"计算价差时出现错误: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(calculate_spread_and_warn, 'interval', minutes=5)    # 设置定时任务，每隔 5 分钟执行一次
    scheduler.start()
    logging.info("定时任务已启动")
