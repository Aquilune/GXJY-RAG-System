# scraper/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.batch_query, name='batch-query'),
    # path('export/', views.export_excel, name='export-excel'),
]