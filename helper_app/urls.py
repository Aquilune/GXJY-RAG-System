from django.urls import path, re_path
from .views import *

urlpatterns = [
    # 根路径映射到 filter_view 视图函数
    path('chatslist/', getChatsList, name='chatsList'),
    path(f'chat/')
]

