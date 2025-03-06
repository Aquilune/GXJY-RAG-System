from django.shortcuts import render
from .models import ProductData, Products

def filter_view(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        batch_number = request.GET.get('batch_number')
        production_area = request.GET.get('production_area')
        # 其他筛选条件...

        queryset = ProductData.objects.all()

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if batch_number:
            queryset = queryset.filter(batch_number=batch_number)
        if production_area:
            queryset = queryset.filter(production_area=production_area)
        # 其他筛选逻辑...

        products = Products.objects.all()
        return render(request, 'filter.html', {'data': queryset, 'products': products})
    products = Products.objects.all()
    return render(request, 'filter.html', {'products': products})