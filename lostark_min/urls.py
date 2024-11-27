# lostark_project/urls.py

from django.contrib import admin
from django.urls import path, include  # include 함수 임포트

urlpatterns = [
    path('admin/', admin.site.urls),
    path('market/', include('lostark_market.urls')),
]
