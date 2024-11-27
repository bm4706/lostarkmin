from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'recent_price', 'current_min_price', 'bundle_count', 'yday_avg_price')
