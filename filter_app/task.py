from django.db import IntegrityError

from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

from .configurations import *
from .models import ProductData

from celery import shared_task

from .configurations import CRAWLER_PAGES
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task(bind=True)
def crawl_data(self, task_id):
    print("开始爬虫")
    # 配置 Chrome 选项以启用无头模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 启用无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用 GPU 加速，避免一些可能的问题

    # 创建带有配置选项的 WebDriver 实例
    driver = webdriver.Chrome(options=chrome_options)

    # 登录
    url = CRAWLER_LOGIN['url']
    username = CRAWLER_LOGIN['username']
    password = CRAWLER_LOGIN['password']

    driver.get(url)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='text']").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='password']").send_keys(password)
    driver.find_element(By.CLASS_NAME, 'info-btn').click()
    time.sleep(2)

    # 访问目标网页
    target_url = CRAWLER_TARGET
    driver.get(target_url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.el-table__row")))

    channel_layer = get_channel_layer()
    # 总页数
    total_pages = CRAWLER_PAGES
    # 对每一页执行数据抓取和翻页
    for page in range(1, total_pages + 1):
        print(f"开始爬第{page}页")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.el-table__row")))

        # 解析页面并抓取数据
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all('tr', class_='el-table__row')
        for row in rows:

            # 批号
            batch_number = row.select_one(".batchNo_line div").text.strip() if row.select_one(
                ".batchNo_line div") else None

            # 获取当前日期
            today = date.today()

            # 检查日期和批号是否都已存在
            if ProductData.objects.filter(batch_number=batch_number, update_date=today).exists():
                print(f"批号 {batch_number} 在日期 {today} 已存在，跳过该条数据")
                continue

            # 产地
            producer_border = row.select_one("td.el-table_1_column_4 .producer-border")
            producer_border_text = producer_border.get_text(strip=True) if producer_border else None

            # 按前两个字拆分产地
            production_area = producer_border_text[:2] if producer_border_text else None
            remaining_origin = producer_border_text[2:] if producer_border_text and len(
                producer_border_text) > 2 else None

            # 类型
            fz13 = row.select_one("td.el-table_1_column_4 .fz13")
            fz13_text = fz13.get_text(strip=True) if fz13 else None

            # 颜色级
            color_grade = row.select_one(".color-level").text.strip() if row.select_one(".color-level") else None

            # 长度、强力、码值、回潮、含杂、长整
            spans = row.find_all('span', class_='fz16')
            length, strength, code_value, moisture_regain, inclusion, long_integrity = (spans[i].text.strip() for i in
                                                                                        range(6)) if len(
                spans) >= 6 else (
                                     None,) * 6

            # 重量
            fz16 = row.select_one("td.el-table_1_column_12 .fz16")
            fz16_text = fz16.get_text(strip=True) if fz16 else None

            try:
                weight = float(fz16_text) if fz16_text else None
                if weight is not None and weight < 38:
                    print(f"批号 {batch_number}，重量 {weight} 小于 38，跳过该条数据")
                    continue
            except ValueError:
                print(f"批号 {batch_number}，重量数据无法转换为数字，跳过该条数据")
                continue

            # 仓库
            ell_bold_blue_pointer = row.select_one("td.el-table_1_column_13 .ell.bold.blue.pointer")
            ell_bold_blue_pointer_text = ell_bold_blue_pointer.get_text(strip=True) if ell_bold_blue_pointer else None

            # 报价方式
            deal_type_element = row.select_one("td.el-table_1_column_14 .dt-div")
            deal_type = deal_type_element.text.strip() if deal_type_element else None

            # 初始化三部分为空
            deal_type_part1, deal_type_part2, deal_type_part3 = None, None, None

            if deal_type:
                import re

                # 针对两种格式的正则表达式匹配
                match = re.match(r'(\D+)?(\d+)([+-]\d+)?', deal_type)
                if match:
                    deal_type_part1 = match.group(1).strip() if match.group(1) else "点价"  # 提取第一部分（可能是文字或空）
                    deal_type_part2 = match.group(2).strip() if match.group(2) else None  # 提取数字部分
                    deal_type_part3 = match.group(3).strip() if match.group(3) else None  # 提取增量（可能为空）

            # 出库基差
            out_difference = row.select_one(".el-table_1_column_15 .cell").text.strip() if row.select_one(
                ".el-table_1_column_15 .cell") else None

            # 出价
            offer_price = row.select_one(".el-table_1_column_16 .cell").text.strip() if row.select_one(
                ".el-table_1_column_16 .cell") else None

            # 结算
            settlement = row.select_one(".el-table_1_column_17 .cell").text.strip() if row.select_one(
                ".el-table_1_column_17 .cell") else None

            # 运费
            freight = row.select_one(".el-table_1_column_18 .cell").text.strip() if row.select_one(
                ".el-table_1_column_18 .cell") else None

            # 预估送到价
            estimated_delivery_price = row.select_one(
                ".el-table_1_column_19 .cell span.bold").text.strip() if row.select_one(
                ".el-table_1_column_19 .cell span.bold") else None

            # 卖家出库费
            seller_outbound_fee = row.select_one(".el-table_1_column_20 .cell").text.strip() if row.select_one(
                ".el-table_1_column_20 .cell") else None

            # 处理报价方式3字段
            quotation_method3_str = str(deal_type_part3)

            # 检查是否为特殊值，如 'None' 或空字符串
            if quotation_method3_str == 'None' or pd.isna(quotation_method3_str) or quotation_method3_str == '':
                deal_type_part3 = None
            elif quotation_method3_str.startswith('+'):
                try:
                    deal_type_part3 = float(quotation_method3_str[1:])
                except ValueError:
                    deal_type_part3 = None
            elif quotation_method3_str.startswith('-'):
                try:
                    deal_type_part3 = -float(quotation_method3_str[1:])
                except ValueError:
                    deal_type_part3 = None
            else:
                try:
                    deal_type_part3 = float(quotation_method3_str)
                except ValueError:
                    deal_type_part3 = None

            # 处理出库基差列
            # 去除 "在途" 字段
            outbound_basis_str = str(out_difference).replace('在途', '')
            if pd.isna(outbound_basis_str) or outbound_basis_str == '':
                outbound_basis = None
            else:
                try:
                    outbound_basis = int(outbound_basis_str)
                except ValueError:
                    outbound_basis = None

            # 处理出价列
            if offer_price == '':
                bid = None
            else:
                try:
                    bid = int(offer_price)
                except ValueError:
                    bid = None

            # 处理报价方式2列
            if pd.isna(deal_type_part2) or deal_type_part2 == '':
                quotation_method2 = None
            else:
                try:
                    quotation_method2 = int(deal_type_part2)
                except (ValueError, TypeError):
                    quotation_method2 = None

            # 获取当前日期
            today = date.today()
            try:
                product = ProductData(
                    batch_number=batch_number,
                    production_area=production_area,
                    production_place=remaining_origin,
                    type=fz13_text,
                    color_grade=color_grade,
                    length=length,
                    strength=strength,
                    code_value=code_value,
                    moisture_regain=moisture_regain,
                    impurity_content=inclusion,
                    length_uniformity=long_integrity,
                    weight=fz16_text,
                    warehouse=ell_bold_blue_pointer_text,
                    quotation_method=deal_type_part1,
                    quotation_method2=quotation_method2,
                    quotation_method3=deal_type_part3,
                    outbound_basis=outbound_basis,
                    update_date=today,
                    bid=bid,
                    settlement=settlement,
                    freight=freight
                )
                product.save()
                print(f"批号 {batch_number}，日期 {today}，插入成功")
            except IntegrityError:
                print(f"批号 {batch_number}，日期 {today}，插入出错")
                continue

        print(f"第{page}页已获取完毕。")

        # 检查是否已经到达最后一页
        if page == total_pages:
            print("已达到设置的总页数")
            break

        # 尝试翻页
        try:
            # 等待页面加载并获取所有的下一页按钮
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button.el-button.first-pager.el-button--default:not(.is-disabled)"))
            )
            next_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                "button.el-button.first-pager.el-button--default:not(.is-disabled)")

            found_next_page = False
            for button in next_buttons:
                if '下一页' in button.text:
                    # 滚动到按钮的位置
                    driver.execute_script("arguments[0].scrollIntoView();", button)

                    # 使用JavaScript点击按钮，避免遮挡问题
                    driver.execute_script("arguments[0].click();", button)

                    time.sleep(2)  # 等待页面加载
                    found_next_page = True
                    break

            if not found_next_page:
                print(f"End of pages reached at page {page}")
                break
        except NoSuchElementException:
            print(f"End of pages reached at page {page}")
            break
        except StaleElementReferenceException:
            continue

        progress = (page / total_pages) * 100
        print(f"Progress: {progress}")
        self.update_state(state='PROGRESS', meta={'progress': progress})

        # 通过 WebSocket 发送进度信息
        async_to_sync(channel_layer.group_send)(
            f'progress_{task_id}',
            {
                'type': 'send_progress',
                'progress': progress
            }
        )

    # 任务完成
    async_to_sync(channel_layer.group_send)(
        f'progress_{task_id}',
        {
            'type': 'send_progress',
            'progress': 100
        }
    )
    # 关闭浏览器
    driver.quit()
