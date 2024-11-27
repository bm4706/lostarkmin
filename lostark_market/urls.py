from django.urls import path
from .views import fetch_material_prices, calculate_profit

urlpatterns = [
    path('fetch-prices/', fetch_material_prices, name='fetch_prices'),
    path('calculate-profit/', calculate_profit, name='calculate_profit'),
]
