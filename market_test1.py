"""
거래소에서 아이템 정보 추출하는 코드입니다.

json_data에서 CategoryCode와 itemname부분을 원하는 값으로 변경합니다.

그리고 파이썬을 실행시키면 입력값과 일치하는 결과물들을 하나씩 보여줍니다.


"""

import requests
import json
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 토큰 가져오기
Token = os.getenv('LOSTARK_API_TOKEN')

headers = {
    'accept': 'application/json',
    'authorization': f'Bearer {Token}',
    'Content-Type': 'application/json',
}

json_data = {
    'Sort': 'GRADE',
    'CategoryCode': 50010,
    'ItemName': '융화',
    'PageNo': 0,
    'SortCondition': 'ASC',
}

# {
#   "Sort": "GRADE",
#   "CategoryCode": 90700,
#   "ItemName": "유물",
#   "PageNo": 0,
#   "SortCondition": "ASC"
# }

response = requests.post('https://developer-lostark.game.onstove.com/markets/items', headers=headers, json=json_data)

# 응답 상태 코드 확인
print(f"Response Status Code: {response.status_code}")

if response.status_code == 200:
    # JSON 응답 데이터를 보기 좋게 출력
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 전체 응답 출력

    # 개별 아이템 정보 출력
    print("\n--- 검색된 아이템 목록 ---")
    items = data.get("Items", [])
    for item in items:
        print(f"아이템 이름: {item['Name']}")
        print(f"아이템 등급: {item['Grade']}")
        print(f"아이콘 URL: {item['Icon']}")
        print(f"번들 개수: {item['BundleCount']}")
        print(f"어제 평균 가격: {item['YDayAvgPrice']} 골드")
        print(f"최근 거래 가격: {item['RecentPrice']} 골드")
        print(f"현재 최저 가격: {item['CurrentMinPrice']} 골드")
        print("-" * 40)
else:
    print("API 요청 실패")
    print(response.text)
