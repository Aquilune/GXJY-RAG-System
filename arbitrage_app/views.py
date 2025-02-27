import json

from django.http import JsonResponse
from .models import ArbitrageData
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import ArbitrageData
from WindPy import w
import datetime

@csrf_exempt
def calculate_arbitrage(request):
    if request.method == 'POST':
        # 启动 WindPy
        w.start()
        if w.isconnected():
            try:
                # 解析 JSON 数据
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
                delivery_date_str = data.get('delivery_date')

                # 检查 delivery_date_str 是否为 None
                if delivery_date_str is None:
                    return HttpResponse("缺少 delivery_date 字段", status=400)

                delivery_date = datetime.datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
                inter_period_time = int(data.get('inter_period_time'))

                # 创建 ArbitrageData 实例
                arbitrage_data = ArbitrageData(
                    storage_fee=storage_fee,
                    trading_fee=trading_fee,
                    delivery_fee=delivery_fee,
                    capital_cost=capital_cost,
                    vat=vat,
                    stamp_duty=stamp_duty,
                    cost_tax=cost_tax,
                    delivery_date=delivery_date,
                    inter_period_time=inter_period_time
                )
                # 调用重写的 save 方法保存数据
                arbitrage_data.save(near_code, far_code)
                return HttpResponse("数据保存成功！")
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                return HttpResponse(f"数据解析错误: {str(e)}", status=400)
        else:
            return HttpResponse("WindPy 连接失败，请检查网络或授权。")
        return HttpResponse("请使用 POST 请求。")