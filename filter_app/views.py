import json

import numpy as np
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from .models import ProductData

from django.http import JsonResponse
from .crawler import crawl_data


def trigger_crawl(request):
    try:
        crawl_data()
        return JsonResponse({'status': 'success', 'message': '数据获取任务已完成'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def filter_view(request):
    queryset = ProductData.objects.all()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            batch_number = data.get('batch_number')
            production_area = data.get('production_area')
            product_place = data.get('product_place')
            type = data.get('type')
            lengthMax = data.get('lengthMax')
            lengthMin = data.get('lengthMin')
            strengthMax = data.get('strengthMax')
            strengthMin = data.get('strengthMin')
            code_valueMax = data.get('code_valueMax')
            code_valueMin = data.get('code_valueMin')
            moisture_regainMax = data.get('moisture_regainMax')
            moisture_regainMin = data.get('moisture_regainMin')
            impurity_contentMax = data.get('impurity_contentMax')
            impurity_contentMin = data.get('impurity_contentMin')
            length_uniformityMax = data.get('length_uniformityMax')
            length_uniformityMin = data.get('length_uniformityMin')
            weightMax = data.get('weightMax')
            weightMin = data.get('weightMin')
            warehouse = data.get('warehouse')

            if batch_number:
                queryset = queryset.filter(batch_number=batch_number)
            if production_area:
                queryset = queryset.filter(production_area=production_area)
            if product_place:
                queryset = queryset.filter(product_place=product_place)
            if type:
                queryset = queryset.filter(type=type)
            if lengthMax:
                queryset = queryset.filter(length__lte=lengthMax)
            if lengthMin:
                queryset = queryset.filter(length__gte=lengthMin)
            if strengthMax:
                queryset = queryset.filter(strength__lte=strengthMax)
            if strengthMin:
                queryset = queryset.filter(strength__gte=strengthMin)
            if code_valueMax:
                queryset = queryset.filter(code_value__lte=code_valueMax)
            if code_valueMin:
                queryset = queryset.filter(code_value__gte=code_valueMin)
            if moisture_regainMax:
                queryset = queryset.filter(moisture_regain__lte=moisture_regainMax)
            if moisture_regainMin:
                queryset = queryset.filter(moisture_regain__gte=moisture_regainMin)
            if impurity_contentMax:
                queryset = queryset.filter(impurity_content__lte=impurity_contentMax)
            if impurity_contentMin:
                queryset = queryset.filter(impurity_content__gte=impurity_contentMin)
            if length_uniformityMax:
                queryset = queryset.filter(length_uniformity__lte=length_uniformityMax)
            if length_uniformityMin:
                queryset = queryset.filter(length_uniformity__gte=length_uniformityMin)
            if weightMax:
                queryset = queryset.filter(weight__lte=weightMax)
            if weightMin:
                queryset = queryset.filter(weight__gte=weightMin)
            if warehouse:
                queryset = queryset.filter(warehouse=warehouse)

            # # 创建 Paginator 对象，每页显示 10 条数据（可根据需求调整）
            # paginator = Paginator(queryset, 10)
            #
            # # 获取当前页码，默认为第 1 页
            # page_number = request.GET.get('page', 1)
            # page_obj = paginator.get_page(page_number)

            data = [model_to_dict(item) for item in queryset]

            return JsonResponse({'data': data}, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

@csrf_exempt
def comparison_view(request):
    queryset = ProductData.objects.all()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            dateMin = data.get('dateMin')
            dateMax = data.get('dateMax')
            lengthMax = data.get('lengthMax')
            lengthMin = data.get('lengthMin')
            strengthMax = data.get('strengthMax')
            strengthMin = data.get('strengthMin')
            code_valueMax = data.get('code_valueMax')
            code_valueMin = data.get('code_valueMin')
            moisture_regainMax = data.get('moisture_regainMax')
            moisture_regainMin = data.get('moisture_regainMin')
            impurity_contentMax = data.get('impurity_contentMax')
            impurity_contentMin = data.get('impurity_contentMin')
            length_uniformityMax = data.get('length_uniformityMax')
            length_uniformityMin = data.get('length_uniformityMin')
            weightMax = data.get('weightMax')
            weightMin = data.get('weightMin')

            if dateMin:
                queryset = queryset.filter(update_date__gte=dateMin)
            if dateMax:
                queryset = queryset.filter(update_date__lte=dateMax)
            if lengthMax:
                queryset = queryset.filter(length__lte=lengthMax)
            if lengthMin:
                queryset = queryset.filter(length__gte=lengthMin)
            if strengthMax:
                queryset = queryset.filter(strength__lte=strengthMax)
            if strengthMin:
                queryset = queryset.filter(strength__gte=strengthMin)
            if code_valueMax:
                queryset = queryset.filter(code_value__lte=code_valueMax)
            if code_valueMin:
                queryset = queryset.filter(code_value__gte=code_valueMin)
            if moisture_regainMax:
                queryset = queryset.filter(moisture_regain__lte=moisture_regainMax)  # 修正字段名
            if moisture_regainMin:
                queryset = queryset.filter(moisture_regain__gte=moisture_regainMin)  # 修正字段名
            if impurity_contentMax:
                queryset = queryset.filter(impurity_content__lte=impurity_contentMax)
            if impurity_contentMin:
                queryset = queryset.filter(impurity_content__gte=impurity_contentMin)
            if length_uniformityMax:
                queryset = queryset.filter(length_uniformity__lte=length_uniformityMax)
            if length_uniformityMin:
                queryset = queryset.filter(length_uniformity__gte=length_uniformityMin)
            if weightMax:
                queryset = queryset.filter(weight__lte=weightMax)
            if weightMin:
                queryset = queryset.filter(weight__gte=weightMin)

            queryset = queryset.filter(quotation_method="点价")

            # 按日期分组
            date_groups = {}
            for item in queryset:
                date = item.update_date
                if date not in date_groups:
                    date_groups[date] = []
                date_groups[date].append(item.outbound_basis)


            # 计算每个日期的中位数和 25%-75% 分位数区间
            chart_data = []
            for date, basis_values in date_groups.items():
                if basis_values:
                    median = np.median(basis_values)
                    max = np.max(basis_values)
                    min = np.min(basis_values)
                    q25, q75 = np.percentile(basis_values, [25, 75])
                    chart_data.append({
                        'date': str(date),
                        'median': float(median),
                        'max': float(max),
                        'min': float(min),
                        'q25': float(q25),
                        'q75': float(q75),
                        'volume': len(basis_values)
                    })

            # 按日期排序
            chart_data.sort(key=lambda x: x['date'])

            return JsonResponse({'chart_data': chart_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)





