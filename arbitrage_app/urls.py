from django.urls import path
from .views import calculate_arbitrage

urlpatterns = [
    path('calculate/', calculate_arbitrage, name='calculate_arbitrage'),
]