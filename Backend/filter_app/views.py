import json
import uuid

import numpy as np
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

# from .configurations import SINGLE_PAGE_NUM
from .models import ProductData

from .task import crawl_data
from django.http import JsonResponse
from django.db.models import Q

@csrf_exempt


def trigger_crawl(request):
    try:
        # task_id = str(uuid.uuid4())
        # print(f"Task {task_id} sent to Celery. Task ID in Celery: {task_id}")
        # 异步调用 crawl_data 任务
        # crawl_data.delay(task_id)
        crawl_data()
        # return JsonResponse({'status': 'success', 'task_id': task_id})
        return JsonResponse({'status': 'success'})
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

            # 获取分页参数
            page = data.get('page', 1)  # 默认页码为 1
            page_size = data.get('page_size')  # 默认每页显示记录数

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

            # 创建 Paginator 实例
            paginator = Paginator(queryset, page_size)
            print(page_size)
            try:
                # 获取指定页码的分页数据
                page_obj = paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                # 如果页码不是整数或超出范围，返回第一页数据
                page_obj = paginator.page(1)

            # 将分页数据转换为字典列表
            data = [model_to_dict(item) for item in page_obj]

            # 构建分页信息
            pagination_info = {
                'page_size': page_size,
                'total_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'total_count': paginator.count
            }

            # 返回分页数据和分页信息
            return JsonResponse({
                'data': data,
                'pagination': pagination_info
            }, safe=False)

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
            region = data.get('region')
            place = data.get('place')
            type_ = data.get('type')  # 避免使用 Python 关键字 type
            warehouseArea = data.get('warehouse_area')
            quotation_method = data.get('quotation_method')

            # 将字符串转换为列表
            region_list = region.split(',') if region else []
            place_list = place.split(',') if place else []
            type_list = type_.split(',') if type_ else []
            warehouseArea_list = warehouseArea.split(',') if warehouseArea else []
            quotation_method_list = quotation_method.split(',') if quotation_method else []

            quotation_method_conditions = []
            quotation_method2_conditions = []

            for method in quotation_method_list:
                if method == '一口价':
                    # 一口价
                    quotation_method_conditions.append('一口价')
                elif method.startswith('点价-'):
                    # 点价-数字，提取数字
                    number = method.replace('点价-', '')
                    if number.isdigit():
                        quotation_method2_conditions.append(int(number))

            if quotation_method_conditions and quotation_method2_conditions:
                queryset = queryset.filter(
                    (
                        Q(quotation_method__in=quotation_method_conditions)
                    ) | (
                        Q(quotation_method='点价', quotation_method2__in=quotation_method2_conditions)
                    )
                )
            elif quotation_method_conditions:
                queryset = queryset.filter(quotation_method__in=quotation_method_conditions)
            elif quotation_method2_conditions:
                queryset = queryset.filter(quotation_method='点价', quotation_method2__in=quotation_method2_conditions)

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
            yearMax = data.get('yearMax')
            yearMin = data.get('yearMin')


            if region_list:
                queryset = queryset.filter(production_area__in=region_list)
            if place_list:
                queryset = queryset.filter(production_place__in=place_list)
            if type_list:
                queryset = queryset.filter(type__in=type_list)
            if warehouseArea:
                queryset = queryset.filter(warehouse_area__in=warehouseArea_list)
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
            if yearMax:
                queryset = queryset.filter(batch_product_year__lte=yearMax)
            if yearMin:
                queryset = queryset.filter(batch_product_year__gte=yearMin)

            # queryset = queryset.filter(quotation_method="点价")

            # 按日期分组
            # 按日期分组
            date_groups = {}
            for item in queryset:
                date = item.update_date
                if date not in date_groups:
                    date_groups[date] = []

                basis_value = item.outbound_basis
                if item.quotation_method == '一口价':
                    basis_value = item.quotation_method2

                    # 超过10000跳过
                    if float(basis_value) > 10000:
                        continue

                # 尝试转成浮点数
                try:
                    basis_value = float(basis_value)
                except (TypeError, ValueError):
                    # 转换失败，比如是None或者空字符串，跳过
                    continue


                date_groups[date].append((basis_value, item.weight))

                date_groups[date].append((basis_value, item.weight))


            # 计算每个日期的中位数和 25%-75% 分位数区间
            chart_data = []
            for date, values in date_groups.items():
                if values:
                    # 分离出库基差和重量
                    basis_values = [value[0] for value in values]
                    weight_values = [value[1] for value in values]

                    median = np.median(basis_values)
                    max = np.max(basis_values)
                    min = np.min(basis_values)
                    q25, q75 = np.percentile(basis_values, [25, 75])
                    total_weight = np.sum(weight_values)
                    chart_data.append({
                        'date': str(date),
                        'median': float(median),
                        'max': float(max),
                        'min': float(min),
                        'q25': float(q25),
                        'q75': float(q75),
                        'volume': len(basis_values),
                        'total_weight': float(total_weight)
                    })

            # 按日期排序
            chart_data.sort(key=lambda x: x['date'])

            return JsonResponse({'chart_data': chart_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


@csrf_exempt
def delete_data_by_date(request, date):
    if request.method == 'DELETE':
        try:
            if not date:
                return JsonResponse({'error': 'Date parameter is required'}, status=400)

            # 删除指定日期的数据
            deleted_count, _ = ProductData.objects.filter(update_date=date).delete()

            return JsonResponse({'message': f'{deleted_count} records deleted successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


@csrf_exempt
def get_quotation_methods(request):
    if request.method == 'GET':
        # 查询所有的quotation_method和quotation_method2
        records = ProductData.objects.values('quotation_method', 'quotation_method2').distinct()

        methods = []

        # 先加上固定的一口价
        methods.append({
            'label': '一口价',
            'value': '一口价'
        })

        # 加上点价-数字的组合
        for record in records:
            if record['quotation_method'] == '点价' and record['quotation_method2'] is not None:
                methods.append({
                    'label': f"点价-{record['quotation_method2']}",
                    'value': f"点价-{record['quotation_method2']}"
                })

        return JsonResponse({'quotation_methods': methods}, safe=False)

    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)