from django.urls import path
from .views import CottonConfigAPI, CertificateAPI, CertificateUploadAPI

urlpatterns = [
    # 配置管理
    path('configs/', CottonConfigAPI.as_view(), name='config-list'),
    path('configs/<uuid:config_id>/', CottonConfigAPI.as_view(), name='config-detail'),

    # 证书管理
    path('certificates/', CertificateAPI.as_view(), name='cert-list'),
    path('certificates/<uuid:cert_id>/', CertificateAPI.as_view(), name='cert-detail'),
    path('certificates/upload/', CertificateUploadAPI.as_view(), name='cert-upload'),
]