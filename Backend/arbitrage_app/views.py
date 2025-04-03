import json
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .configurations import URL_STYLE_MAPPING, URL_TO_EXCHANGE
from .data_providers import get_data_provider
from .models import ArbitrageData


@csrf_exempt
def calculate_arbitrage(request):
    if request.method != 'POST':
        return JsonResponse({"error": "请求方式错误"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))

        # 解析必填字段
        near_code = data.get('near_code')
        far_code = data.get('far_code')
        trading_fee = float(data.get('trading_fee'))
        delivery_fee = float(data.get('delivery_fee'))
        storage_fee = float(data.get('storage_fee'))
        capital_cost = float(data.get('capital_cost'))
        vat = float(data.get('vat'))

        # 解析日期
        date_range = data.get('dateRange', [])
        if len(date_range) != 2:
            return JsonResponse({"error": "dateRange 格式错误"}, status=400)

        first_delivery_date = datetime.strptime(date_range[0], "%Y-%m-%d").date()
        second_delivery_date = datetime.strptime(date_range[1], "%Y-%m-%d").date()

        # 确保交割日期正确
        if first_delivery_date >= second_delivery_date:
            return JsonResponse({"error": "第一合约交割日期必须早于第二合约交割日期"}, status=400)

        # 计算跨期时间
        inter_period_time = (second_delivery_date - first_delivery_date).days
        if inter_period_time <= 0:
            return JsonResponse({"error": "跨期时间必须大于0"}, status=400)

        # 获取市场价格
        # provider = get_data_provider()
        # near_month_price = provider.get_near_month_price(near_code)
        # far_month_price = provider.get_near_month_price(far_code)
        # print(near_month_price, far_month_price)
        near_month_price = 24.6
        far_month_price = 25.6

        # 计算套利相关数据
        # storage_fee = 0.5 * inter_period_time  # 仓储费用
        stamp_duty = (near_month_price + far_month_price) * 0.0003  # 印花税
        cost_tax = (storage_fee + trading_fee + delivery_fee) / 1.06 * 0.06  # 成本税
        tax = vat + stamp_duty - cost_tax  # 税值
        price_spread = far_month_price - near_month_price  # 价差
        arbitrage_cost = storage_fee + trading_fee + delivery_fee + capital_cost + tax  # 套利成本
        net_spread = price_spread - arbitrage_cost  # 净差价
        annual_return = (net_spread / near_month_price / inter_period_time) * 360 if near_month_price > 0 else 0  # 年收益率

        # 存入数据库
        arbitrage_data = ArbitrageData.objects.create(
            near_month_code=near_code,
            far_month_code=far_code,
            near_month_price=near_month_price,
            far_month_price=far_month_price,
            trading_fee=trading_fee,
            delivery_fee=delivery_fee,
            capital_cost=capital_cost,
            vat=vat,
            first_delivery_date=first_delivery_date,
            second_delivery_date=second_delivery_date,
            inter_period_time=inter_period_time,
            storage_fee=storage_fee,
            stamp_duty=stamp_duty,
            cost_tax=cost_tax,
            tax=tax,
            price_spread=price_spread,
            arbitrage_cost=arbitrage_cost,
            net_spread=net_spread,
            annual_return=annual_return
        )

        return JsonResponse({"message": "套利数据计算成功", "id": arbitrage_data.id})

    except (KeyError, ValueError, json.JSONDecodeError) as e:
        return JsonResponse({"error": f"数据解析错误: {str(e)}"}, status=400)


def fetch_table_data(url, style):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'MsoNormalTable', 'style': style})
    if not table:
        table = soup.find('table')

    # 提取表头
    headers = []
    header_cells = table.find_all(
        'td',
        style=lambda value: value and 'background:#ac0000;' in value.lower()
    )

    for cell in header_cells:
        header_text = cell.get_text(strip=True)
        bold_text = cell.find('b').get_text(strip=True) if cell.find('b') else ''
        if not bold_text:
            span = cell.find('span', {'style': True})
            if span:
                bold_text = span.get_text(strip=True)
        link = cell.find('a')
        if link:
            link_text = link.get_text(strip=True)
            bold_text = bold_text.replace(link_text, '').strip() + ' ' + link_text
        final_text = bold_text or header_text
        final_text = final_text.replace('\n', ' ').replace('\xa0', ' ').strip()
        headers.append(final_text)

    # 提取数据行
    data = []
    for row in table.find_all('tr')[1:]:
        row_data = []
        for td in row.find_all(['td', 'th']):
            content = ' '.join(td.stripped_strings)
            content = content.replace('\n', ' ')
            content = content.replace(' ', '')
            row_data.append(content)
        if len(row_data) == len(headers):
            data.append(row_data)
        else:
            if len(row_data) > len(headers):
                row_data = row_data[:len(headers)]
            else:
                row_data += [''] * (len(headers) - len(row_data))
            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    return df.to_dict(orient='records')


@csrf_exempt
def info_view(request):
    if request.method == 'GET':
        try:
            all_data = {}
            for url, style in URL_STYLE_MAPPING.items():
                data = fetch_table_data(url, style)
                # 使用交易所代号作为键而不是URL
                exchange_code = URL_TO_EXCHANGE[url]
                all_data[exchange_code] = data
            return JsonResponse({
                'status': 'success',
                'data': all_data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)