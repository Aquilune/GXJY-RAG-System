# scraper/views.py
import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
import time

from search_app.configurations import DYB_USERNAME, DYB_PASSWORD

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def batch_query(request):
    """批量查询接口（完整字段版）"""
    try:
        data = json.loads(request.body)
        codes = data.get('codes', [])

        if not codes or not isinstance(codes, list):
            return JsonResponse({'error': '请求格式不正确，需要codes数组'}, status=400)

        results = scrape_full_data(codes)

        return JsonResponse({
            'status': 'success',
            'count': len(results),
            'data': results
        })

    except Exception as e:
        logger.error(f"查询错误: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'服务器错误: {str(e)}'}, status=500)


def scrape_full_data(codes):
    """完整字段数据抓取"""
    driver = None
    try:
        # 浏览器配置
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

        # 登录系统
        login(driver)

        results = []
        for code in codes:
            result = {'仓单号': code}
            try:
                driver.get(f"http://www.dybcotton.com/receipt/single/{code}")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'table')))
                # 基础信息
                result.update({
                    '升贴水': extract_table_data(driver, '升贴水'),
                    '交割库': extract_table_data(driver, '交割库'),
                    '产地': extract_table_data(driver, '产地'),
                    '加工企业': extract_table_data(driver, '加工企业'),
                    '组批批号': extract_table_data(driver, '组批批号'),
                    '平均回潮': extract_table_data(driver, '平均回潮'),
                    '合计公重': extract_table_data(driver, '合计公重'),
                    '平均含杂': extract_table_data(driver, '平均含杂'),
                })

                # 质量指标
                result.update({
                    '长度平均值': extract_length(driver),
                    '马克隆值平均值': extract_micronaire(driver),
                    '长度整齐度平均值': extract_uniformity(driver),
                    '断裂比强度平均值': extract_strength(driver),
                })

                # 颜色级指标
                result.update({
                    '白棉1级': extract_table_data(driver, '白棉1级'),
                    '白棉2级': extract_table_data(driver, '白棉2级'),
                    '白棉3级': extract_table_data(driver, '白棉3级'),
                    '白棉4级': extract_table_data(driver, '白棉4级'),
                    '白棉5级': extract_table_data(driver, '白棉5级'),
                    '淡点污棉1级': extract_table_data(driver, '淡点污棉1级'),
                    '淡点污棉2级': extract_table_data(driver, '淡点污棉2级'),
                    '淡点污棉3级': extract_table_data(driver, '淡点污棉3级'),
                    '淡黄染棉1级': extract_table_data(driver, '淡黄染棉1级'),
                    '淡黄染棉2级': extract_table_data(driver, '淡黄染棉2级'),
                    '淡黄染棉3级': extract_table_data(driver, '淡黄染棉3级'),
                    '黄染棉1级': extract_table_data(driver, '黄染棉1级'),
                    '黄染棉2级': extract_table_data(driver, '黄染棉2级'),
                    '轧工质量': extract_table_data(driver, '轧工质量'),
                })
            except Exception as e:
                result['error'] = f'数据提取失败: {str(e)}'
                logger.warning(f"仓单 {code} 提取失败: {str(e)}")

            results.append(result)
            time.sleep(0.5)  # 防止请求过快

        return results

    finally:
        if driver:
            driver.quit()


# 以下是字段提取辅助函数
def extract_table_data(driver, field_name):
    """通用表格数据提取"""
    try:
        return driver.find_element(
            By.XPATH, f"//td[contains(text(), '{field_name}')]/following-sibling::td"
        ).text.strip()
    except:
        return ''


def extract_length(driver):
    """提取长度平均值"""
    try:
        element = driver.find_element(By.XPATH, "//td[contains(text(), '长度')]")
        return element.text.split('平均值:')[1].split()[0]
    except:
        return ''


def extract_micronaire(driver):
    """提取马克隆值平均值"""
    try:
        element = driver.find_element(By.XPATH, "//td[contains(text(), '马克隆值')]")
        return element.text.split('平均值:')[1].split()[0]
    except:
        return ''


def extract_uniformity(driver):
    """提取长度整齐度平均值"""
    try:
        uniformity_element = driver.find_element(By.XPATH, "//td[contains(text(), '长度整齐度')]")
        uniformity_average = uniformity_element.find_element(By.XPATH,
                                                             "following::td[contains(text(), '平均值')]/following-sibling::td[1]").text
        return uniformity_average
    except:
        return ''


def extract_strength(driver):
    """提取断裂比强度平均值"""
    try:
        strength_element = driver.find_element(By.XPATH, "//td[contains(text(), '断裂比强度')]")
        strength_average = strength_element.find_element(By.XPATH,
                                                         "following::td[contains(text(), '平均值')][2]/following-sibling::td[1]").text
        return strength_average
    except:
        return ''


def login(driver):
    """登录系统"""
    driver.get("http://www.dybcotton.com/auth/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'user_name'))
    ).send_keys(DYB_USERNAME)

    driver.find_element(By.NAME, 'user_pass').send_keys(DYB_PASSWORD)
    driver.find_element(By.ID, 'doLogin').click()
    time.sleep(1)