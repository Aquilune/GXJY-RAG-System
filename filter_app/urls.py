from django.urls import path, re_path

from .consumers import ProgressConsumer
from .views import *

urlpatterns = [
    # 根路径映射到 filter_view 视图函数
    path('filter/', filter_view, name='filter'),
    path('crawler/', trigger_crawl, name='crawler_data'),
    # path('crawler/status/<str:task_id>/', crawler_status, name='crawler_status'),
    path('comparison/', comparison_view, name='comparison_data'),
    path('deleteData/<str:date>/', delete_data_by_date, name='delete_data_by_date')
]

websocket_urlpatterns = [
    re_path(r'ws/progress/(?P<task_id>[^/]+)/$', ProgressConsumer.as_asgi()),
]