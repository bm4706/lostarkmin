from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100)  # 재료 이름
    icon_url = models.URLField()             # 아이콘 URL
    bundle_count = models.IntegerField()     # 번들 개수
    yday_avg_price = models.FloatField()     # 어제 평균 가격
    recent_price = models.FloatField()       # 최근 거래 가격
    current_min_price = models.FloatField()  # 현재 최저 가격
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 저장 시간
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


