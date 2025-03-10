from django.urls import path
from .views import *

urlpatterns = [
    # 根路径映射到 filter_view 视图函数
    path('filter/', filter_view, name='filter'),
    path('crawler_data/', trigger_crawl, name='crawler_data'),
    path('comparison/', comparison_view, name='comparison_data')
]