import chinese_calendar as calendar
from datetime import date, timedelta


def get_last_trading_day(year, month):
    day_count = 0
    current_day = date(year, month, 1)
    while True:
        if calendar.is_workday(current_day):
            day_count += 1
            if day_count == 10:
                return current_day
        current_day += timedelta(days=1)
        if current_day.month != month:
            break
    return None


def get_last_delivery_day(last_trading_day):
    if last_trading_day is None:
        return None
    day_count = 0
    current_day = last_trading_day + timedelta(days=1)
    while day_count < 3:
        if calendar.is_workday(current_day):
            day_count += 1
        current_day += timedelta(days=1)
    return current_day - timedelta(days=1)


# 示例：计算 2025 年 3 月的最后交易日和最后交割日
year = 2024
month = 9

last_trading_day = get_last_trading_day(year, month)
last_delivery_day = get_last_delivery_day(last_trading_day)

if last_trading_day is not None:
    print(f"合约月份 {year}-{month} 的最后交易日是: {last_trading_day.strftime('%Y-%m-%d')}")
else:
    print(f"合约月份 {year}-{month} 无法计算最后交易日。")

if last_delivery_day is not None:
    print(f"合约月份 {year}-{month} 的最后交割日是: {last_delivery_day.strftime('%Y-%m-%d')}")
else:
    print(f"合约月份 {year}-{month} 无法计算最后交割日。")