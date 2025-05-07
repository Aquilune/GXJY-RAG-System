from django.urls import path
from . import views
from .views import CertificateUploadView

urlpatterns = [
    path('configs/', views.cotton_config_view),  # GET列表/POST创建
    path('configs/<int:config_id>/', views.cotton_config_view),  # GET详情/DELETE删除
    path('upload/', CertificateUploadView.as_view()),
]