from django.urls import path
from .views import calculate_arbitrage, info_view

urlpatterns = [
    path('calculate/', calculate_arbitrage, name='calculate_arbitrage'),
    path('info/', info_view, name='info_view'),
]