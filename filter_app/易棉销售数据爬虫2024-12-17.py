#!/usr/bin/env python
# coding: utf-8

# In[9]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re  # 导入正则表达式模块

# 创建WebDriver实例
driver = webdriver.Chrome()

# 登录
url = "https://www.oureway.com/users/login"
username = "18516175174"
password = "13919407312"
driver.get(url)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='text']").send_keys(username)
driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='password']").send_keys(password)
driver.find_element(By.CLASS_NAME, 'info-btn').click()
time.sleep(2)

# 访问目标网页
target_url = "https://www.oureway.com/market/resources/xj"
driver.get(target_url)
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.el-table__row")))


# 初始化数据存储列表
data = []

# 总页数（根据实际情况调整）
total_pages = 5 # 这里设置为您需要抓取的总页数

# 对每一页执行数据抓取和翻页
for page in range(1, total_pages + 1):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.el-table__row")))

    # 解析页面并抓取数据
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr', class_='el-table__row')
    for row in rows:
        
        # 批号
        batch_number = row.select_one(".batchNo_line div").text.strip() if row.select_one(".batchNo_line div") else None

        # 产地
        producer_border = row.select_one("td.el-table_1_column_4 .producer-border")
        producer_border_text = producer_border.get_text(strip=True) if producer_border else None

        # 按前两个字拆分产地
        production_area = producer_border_text[:2] if producer_border_text else None
        remaining_origin = producer_border_text[2:] if producer_border_text and len(producer_border_text) > 2 else None

        # 类型
        fz13 = row.select_one("td.el-table_1_column_4 .fz13")
        fz13_text = fz13.get_text(strip=True) if fz13 else None

        # 添加到数据列表
        data.append({
            '批号': batch_number,
            '产区': production_area,
            '产地': remaining_origin,
            '类型': fz13_text,
            # 其他字段保持不变
        })

    # 检查是否已经到达最后一页
    if page == total_pages:
        print("已达到设置的总页数")
        break

    # 尝试翻页
    try:
        # 等待页面加载并获取所有的下一页按钮
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.el-button.first-pager.el-button--default:not(.is-disabled)"))
        )
        next_buttons = driver.find_elements(By.CSS_SELECTOR, "button.el-button.first-pager.el-button--default:not(.is-disabled)")

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



# 关闭浏览器
driver.quit()

# 转换数据为DataFrame
df = pd.DataFrame(data)

# 保存数据到Excel
df.to_excel("易棉购数据12-12.xlsx", index=False)



# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re  # 导入正则表达式模块

# 创建WebDriver实例
driver = webdriver.Chrome()

# 登录
url = "https://www.oureway.com/users/login"
username = "18516175174"
password = "13919407312"
driver.get(url)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='text']").send_keys(username)
driver.find_element(By.CSS_SELECTOR, "input.el-input__inner[type='password']").send_keys(password)
driver.find_element(By.CLASS_NAME, 'info-btn').click()
time.sleep(2)

# 访问目标网页
target_url = "https://www.oureway.com/market/resources/xj"
driver.get(target_url)
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.el-table__row")))


# 初始化数据存储列表
data = []

# 总页数（根据实际情况调整）
total_pages = 574 # 这里设置为您需要抓取的总页数

# 对每一页执行数据抓取和翻页
for page in range(1, total_pages + 1):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.el-table__row")))

    # 解析页面并抓取数据
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr', class_='el-table__row')
    for row in rows:
        
        # 批号
        batch_number = row.select_one(".batchNo_line div").text.strip() if row.select_one(".batchNo_line div") else None

        # 产地
        producer_border = row.select_one("td.el-table_1_column_4 .producer-border")
        producer_border_text = producer_border.get_text(strip=True) if producer_border else None

        # 按前两个字拆分产地
        production_area = producer_border_text[:2] if producer_border_text else None
        remaining_origin = producer_border_text[2:] if producer_border_text and len(producer_border_text) > 2 else None

        # 类型
        fz13 = row.select_one("td.el-table_1_column_4 .fz13")
        fz13_text = fz13.get_text(strip=True) if fz13 else None

        # 颜色级
        color_grade = row.select_one(".color-level").text.strip() if row.select_one(".color-level") else None

        # 长度、强力、码值、回潮、含杂、长整
        spans = row.find_all('span', class_='fz16')
        length, strength, code_value, moisture_regain, inclusion, long_integrity = (spans[i].text.strip() for i in range(6)) if len(spans) >= 6 else (None,) * 6

        # 重量
        fz16 = row.select_one("td.el-table_1_column_12 .fz16")
        fz16_text = fz16.get_text(strip=True) if fz16 else None

        # 仓库
        ell_bold_blue_pointer = row.select_one("td.el-table_1_column_13 .ell.bold.blue.pointer")
        ell_bold_blue_pointer_text = ell_bold_blue_pointer.get_text(strip=True) if ell_bold_blue_pointer else None


        # 报价方式
        #bold = row.select_one("td.el-table_1_column_14 .bold")
        #bold_text = bold.get_text(strip=True) if bold else None
        #deal_type = row.select_one("td.el-table_1_column_14 .dt-div")  # 定位到包含目标数据的 div
        #deal_type_text = deal_type.get_text(strip=True) if deal_type else None
       # deal_type = row.select_one("td.el-table_1_column_14 .dt-div").text.strip() if row.select_one("td.el-table_1_column_14 .dt-div") else None
        #deal_type_part1, deal_type_part2, deal_type_part3 = (None, None, None)  # 初始化为空
        #if deal_type:
           # deal_parts = deal_type.split()  # 按空格拆分字符串
           # deal_type_part1 = deal_parts[0] if len(deal_parts) > 0 else None  # 第一部分
          #  deal_type_part2 = deal_parts[1] if len(deal_parts) > 1 else None  # 第二部分
           # deal_type_part3 = deal_parts[2] if len(deal_parts) > 2 else None  # 第三部分
        deal_type_element = row.select_one("td.el-table_1_column_14 .dt-div")
        deal_type = deal_type_element.text.strip() if deal_type_element else None

        # 初始化三部分为空
        deal_type_part1, deal_type_part2, deal_type_part3 = None, None, None

        if deal_type:
            import re
            # 针对两种格式的正则表达式匹配
            match = re.match(r'(\D+)?(\d+)([+-]\d+)?', deal_type)
            if match:
                deal_type_part1 = match.group(1).strip() if match.group(1) else None  # 提取第一部分（可能是文字或空）
                deal_type_part2 = match.group(2).strip() if match.group(2) else None  # 提取数字部分
                deal_type_part3 = match.group(3).strip() if match.group(3) else None  # 提取增量（可能为空）
        
        
        # 卖方报价
        #dt_div_unit_div = row.select_one("td.el-table_1_column_14 .dt-div.unit-div")
        #dt_div_unit_div_text = dt_div_unit_div.get_text(strip=True) if dt_div_unit_div else None
        
        # 出库基差
        out_difference = row.select_one(".el-table_1_column_15 .cell").text.strip() if row.select_one(".el-table_1_column_15 .cell") else None

        # 出价
        offer_price = row.select_one(".el-table_1_column_16 .cell").text.strip() if row.select_one(".el-table_1_column_16 .cell") else None

        # 结算
        settlement = row.select_one(".el-table_1_column_17 .cell").text.strip() if row.select_one(".el-table_1_column_17 .cell") else None

        # 运费
        freight = row.select_one(".el-table_1_column_18 .cell").text.strip() if row.select_one(".el-table_1_column_18 .cell") else None

        # 预估送到价
        estimated_delivery_price = row.select_one(".el-table_1_column_19 .cell span.bold").text.strip() if row.select_one(".el-table_1_column_19 .cell span.bold") else None

        # 卖家出库费
        seller_outbound_fee = row.select_one(".el-table_1_column_20 .cell").text.strip() if row.select_one(".el-table_1_column_20 .cell") else None

        # 将提取的数据添加到列表
        data.append({
            '批号': batch_number,
            '产区': production_area,
            '产地': remaining_origin,
            '类型': fz13_text,
            '颜色级': color_grade,
            '长度': length,
            '强力': strength,
            '码值': code_value,
            '回潮': moisture_regain,
            '含杂': inclusion,
            '长整': long_integrity,
            '重量': fz16_text,
            '仓库': ell_bold_blue_pointer_text,
            #'报价方式':deal_type,
            '报价方式1': deal_type_part1,  # 存储第一部分
            '报价方式2': deal_type_part2,  # 存储第二部分
            '报价方式3': deal_type_part3,  # 存储第三部分
            #'卖方报价': dt_div_unit_div_text,
            '出库基差': out_difference,
            '出价': offer_price,
            '结算': settlement,
            '运费': freight,
            '预估送到价': estimated_delivery_price,
            '卖家出库费': seller_outbound_fee,
        })

    # 检查是否已经到达最后一页
    if page == total_pages:
        print("已达到设置的总页数")
        break

    # 尝试翻页
    try:
        # 等待页面加载并获取所有的下一页按钮
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.el-button.first-pager.el-button--default:not(.is-disabled)"))
        )
        next_buttons = driver.find_elements(By.CSS_SELECTOR, "button.el-button.first-pager.el-button--default:not(.is-disabled)")

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



# 关闭浏览器
driver.quit()

# 转换数据为DataFrame
df = pd.DataFrame(data)

# 保存数据到Excel
df.to_excel("易棉购数据03-04.xlsx", index=False)


# In[ ]:




