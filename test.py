import requests
import json
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 토큰 가져오기
Token = os.getenv('LOSTARK_API_TOKEN')  # .env 파일의 LOSTARK_API_TOKEN 값

headers = {
    'accept': 'application/json',
    'authorization': f'Bearer {Token}'  # Bearer 추가
}

url = 'https://developer-lostark.game.onstove.com/news/events'

response = requests.get(url, headers=headers)

# 응답 상태 코드 출력
print(f"Response Status Code: {response.status_code}")

if response.status_code == 200:
    # JSON 응답 데이터를 보기 좋게 출력
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 전체 데이터 출력
    
    # 개별 이벤트 정보 출력
    print("\n--- 이벤트 목록 ---")
    for event in data:
        print(f"제목: {event['Title']}")
        print(f"이미지: {event['Thumbnail']}")
        print(f"링크: {event['Link']}")
        print(f"시작일: {event['StartDate']}")
        print(f"종료일: {event['EndDate']}")
        print(f"보상일: {event.get('RewardDate', '없음')}")
        print()
else:
    print("API 요청 실패")
    print(response.text)
