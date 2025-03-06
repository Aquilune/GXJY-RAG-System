from django.urls import path
from .views import filter_view

urlpatterns = [
    # 根路径映射到 filter_view 视图函数
    path('filter/', filter_view, name='filter'),
]