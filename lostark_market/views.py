import requests
from django.http import JsonResponse
from .models import Material
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect
import math
from django.urls import reverse
from django.db.models import Max



def fetch_material_prices(request):
    load_dotenv()

    # 환경 변수에서 토큰 가져오기
    Token = os.getenv('LOSTARK_API_TOKEN') 
        
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {Token}',  # 여기에 실제 API 토큰 입력
        'Content-Type': 'application/json',
    }

    # 필요한 재료와 그들의 카테고리 코드
    materials = [
        {"ItemName": "고대 유물", "CategoryCode": 90700},
        {"ItemName": "희귀한 유물", "CategoryCode": 90700},
        {"ItemName": "오레하 유물", "CategoryCode": 90700},
        {"ItemName": "아비도스 유물", "CategoryCode": 90700},
        {"ItemName": "아비도스 융화 재료", "CategoryCode": 50010},
        {"ItemName": "최상급 오레하 융화 재료", "CategoryCode": 50010},
    ]
    
    
    

    for material in materials:
        json_data = {
            'Sort': 'GRADE',
            'CategoryCode': material["CategoryCode"],
            'ItemName': material["ItemName"],
            'PageNo': 0,
            'SortCondition': 'ASC',
        }

        response = requests.post('https://developer-lostark.game.onstove.com/markets/items', headers=headers, json=json_data)
        if response.status_code == 200:
            data = response.json().get('Items', [])
            if data:
                item = data[0]  # 첫 번째 아이템 정보만 저장
                Material.objects.update_or_create(
                    name=item["Name"],
                    defaults={
                        'icon_url': item["Icon"],
                        'bundle_count': item["BundleCount"],
                        'yday_avg_price': item["YDayAvgPrice"],
                        'recent_price': item["RecentPrice"],
                        'current_min_price': item["CurrentMinPrice"],
                    },
                )

    return redirect(reverse('calculate_profit'))





def calculate_profit(request):
    last_updated = Material.objects.aggregate(Max('updated_at'))['updated_at__max']
    last_updated_formatted = last_updated.strftime("%m/%d %H:%M") if last_updated else "갱신 기록 없음"

    if request.method == 'GET':
        return render(request, 'lostark_market/calculate.html')

    if request.method == 'POST':
        discount = float(request.POST.get('discount', 0)) / 100  # 기본값: 0% 수수료 감소

        # 체크박스 값 처리
        exclude_ancient = 'exclude_ancient' in request.POST
        exclude_rare = 'exclude_rare' in request.POST
        exclude_oreha = 'exclude_oreha' in request.POST
        exclude_abidos = 'exclude_abidos' in request.POST

        # 필요한 재료 정보
        try:
            materials = {
                '고대 유물': Material.objects.get(name="고대 유물"),
                '희귀한 유물': Material.objects.get(name="희귀한 유물"),
                '오레하 유물': Material.objects.get(name="오레하 유물"),
                '아비도스 유물': Material.objects.get(name="아비도스 유물"),
            }
            abidos_crafted = Material.objects.get(name="아비도스 융화 재료")
            oreha_crafted = Material.objects.get(name="최상급 오레하 융화 재료")
        except Material.DoesNotExist:
            return render(request, 'lostark_market/error.html', {'message': '필요한 재료 데이터가 없습니다.'})

        # 제작 정보
        crafted_items = [
            {
                'name': '아비도스 융화 재료',
                'needed_materials': {
                    '고대 유물': 86 if not exclude_ancient else 0,
                    '아비도스 유물': 33 if not exclude_abidos else 0,
                    '희귀한 유물': 45 if not exclude_rare else 0,
                },
                'crafting_fee': 400,
                'selling_price': abidos_crafted.current_min_price,
                'produced_quantity': 10,
                'icon_url': abidos_crafted.icon_url,
            },
            {
                'name': '최상급 오레하 융화 재료',
                'needed_materials': {
                    '고대 유물': 107 if not exclude_ancient else 0,
                    '오레하 유물': 52 if not exclude_oreha else 0,
                    '희귀한 유물': 51 if not exclude_rare else 0,
                },
                'crafting_fee': 300,
                'selling_price': oreha_crafted.current_min_price,
                'produced_quantity': 15,
                'icon_url': oreha_crafted.icon_url,
            },
        ]

        results = []

        # 각 제작 아이템에 대해 계산
        for item in crafted_items:
            total_cost = 0
            for material_name, quantity in item['needed_materials'].items():
                material = materials[material_name]
                price_per_unit = material.recent_price / material.bundle_count
                total_cost += quantity * price_per_unit

            # 제작 수수료 계산
            crafting_fee = item['crafting_fee'] * (1 - discount)
            total_cost += crafting_fee

            # 1개당 제작 비용
            cost_per_unit = total_cost / item['produced_quantity']

            # 경매장 수수료 계산
            auction_fee = math.ceil(item['selling_price'] * 0.05)
            final_amount = item['selling_price'] - auction_fee

            # 이득/손해 계산
            profit_per_unit = final_amount - cost_per_unit

            results.append({
                'name': item['name'],
                'icon_url': item['icon_url'],  # 여기서 가져오는 값이 올바른지 확인
                'total_cost': round(total_cost, 2),
                'cost_per_unit': round(cost_per_unit, 2),
                'selling_price': round(item['selling_price'], 2),
                'auction_fee': round(auction_fee, 2),
                'final_amount': round(final_amount, 2),
                'profit_per_unit': round(profit_per_unit, 2),
                'produced_quantity': item['produced_quantity'],
            })

        # 재료 데이터 추가
        material_info = [
            {
                'name': material.name,
                'icon_url': material.icon_url,
                'recent_price': material.recent_price,
                'bundle_count': material.bundle_count,
                'price_per_unit': round(material.recent_price / material.bundle_count, 2),
            }
            for material in materials.values()
        ]

        return render(request, 'lostark_market/result.html', {
        'results': results,
        'material_info': material_info,
        'last_updated': last_updated_formatted,  # 템플릿에 전달
    })



def fetch_prices(request):
    if request.method == 'POST':
        fetch_material_prices(request)  # 데이터를 갱신하는 함수 호출
        # 결과 페이지로 리디렉션
        return redirect(reverse('calculate_profit'))
    elif request.method == 'GET':
        # GET 요청 시 결과 페이지로 리디렉션
        return redirect(reverse('calculate_profit'))
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
