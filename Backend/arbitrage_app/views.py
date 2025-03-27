import json
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .configurations import URL_STYLE_MAPPING, URL_TO_EXCHANGE
from .models import ArbitrageData


@csrf_exempt
def calculate_arbitrage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            near_code = data.get('near_code')
            far_code = data.get('far_code')
            storage_fee = float(data.get('storage_fee'))
            trading_fee = float(data.get('trading_fee'))
            delivery_fee = float(data.get('delivery_fee'))
            capital_cost = float(data.get('capital_cost'))
            vat = float(data.get('vat'))
            stamp_duty = float(data.get('stamp_duty'))
            cost_tax = float(data.get('cost_tax'))
            first_delivery_date = datetime.strptime(data.get('dateRange')[0], "%Y-%m-%d")
            second_delivery_date = datetime.strptime(data.get('dateRange')[1], "%Y-%m-%d")
            # delivery_date_str = data.get('delivery_date')

            # 检查 delivery_date_str 是否为 None
            # if delivery_date_str is None:
            #     return HttpResponse("缺少 delivery_date 字段", status=400)

            # delivery_date = datetime.datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
            # inter_period_time = int(data.get('inter_period_time'))

            # 创建 ArbitrageData 实例
            arbitrage_data = ArbitrageData(
                near_month_code=near_code,
                far_month_code=far_code,
                storage_fee=storage_fee,
                trading_fee=trading_fee,
                delivery_fee=delivery_fee,
                capital_cost=capital_cost,
                vat=vat,
                stamp_duty=stamp_duty,
                cost_tax=cost_tax,
                first_delivery_date=first_delivery_date,
                second_delivery_date=second_delivery_date
                # delivery_date=delivery_date,
                # inter_period_time=inter_period_time
            )
            # 调用重写的 save 方法保存数据
            arbitrage_data.save(near_code, far_code)
            return HttpResponse("数据保存成功！")
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            return HttpResponse(f"数据解析错误: {str(e)}", status=400)
    else:
        return HttpResponse("WindPy 连接失败，请检查网络或授权。")


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