# 로스트아크 고고학 이익 계산기

Django 기반 웹 애플리케이션으로, 로스트아크 공식 API를 활용해 제작 아이템의 손익을 계산할 수 있습니다. 실시간으로 시장 데이터를 가져와 제작 비용 및 예상 이익을 확인할 수 있습니다.

## 주요 기능

#### 1. 실시간 시장 데이터 조회: 로스트아크 API를 통해 재료 및 아이템의 현재 가격을 가져옵니다.

#### 2. 제작 이익 계산: 입력된 데이터를 바탕으로 제작 비용 및 예상 이익/손해를 계산합니다.
   
#### 3. 경매장 수수료 반영: 경매장 수수료를 포함한 상세 계산 결과를 제공합니다.
   
#### 4. 사용자 친화적인 인터페이스: 간단한 UI로 사용자가 쉽게 이익을 확인할 수 있습니다.

## 기술 스텍

백엔드: Django (Python)

프론트엔드: HTML, CSS (Django 템플릿)

데이터베이스: SQLite (개발), PostgreSQL (배포)

배포: AWS EC2 (Gunicorn + Nginx)

API 연동: 로스트아크 공식 API

## 작동 원리

#### 1. 시장 데이터 가져오기

로스트아크 API를 통해 재료와 아이템의 실시간 시장 데이터를 가져옵니다.

데이터는 데이터베이스에 저장되어 계산 시 사용됩니다.

#### 2. 제작 이익 계산

사용자가 입력한 데이터를 바탕으로 제작 비용, 경매장 수수료, 최종 이익/손해를 계산합니다.

재료를 제외하거나 할인율을 적용할 수 있는 옵션을 제공합니다.

#### 3. 실시간 데이터 업데이트

"데이터 최신" 버튼을 통해 최신 시장 데이터를 가져올 수 있습니다.


## 스크린샷

#### 1. 계산 
![start](https://github.com/user-attachments/assets/7a54cc1e-2528-4d6a-a860-d078112d933d)

본인이 가지고 있는 재료를 체크박스에 체크해서 계산에서 제외하거나 본인의 수수료 감소 퍼센트를 수동으로 입력하고 계산 버튼을 클릭하면 됩니다.

#### 2. 계산 후
![result](https://github.com/user-attachments/assets/817fd794-fc19-4082-9d0b-635fc77b6729)

계산을 통해 본인이 오레하 유물을 제작한다면 1개당 이익(손해)가 얼마만큼 발생하는지 확인 할 수 있습니다.

또한, 데이터 최신 버튼을 통해 실시간으로 변경되는 재료값을 한번 가져오도록합니다.


## 설치 방법

#### 1. 프로젝트 클론
git clone https://github.com/bm4706/lostarkmin.git

cd lostark-market-calculator


#### 2. 가상 환경 설정

python3 -m venv venv

source venv/bin/activate  # Linux/macOS

venv\Scripts\activate     # Windows


#### 3. 패키지 설치

pip install -r requirements.txt


#### 4. 환경 변수 설정

.env 파일 생성후에 본인의 키를 넣으시면 됩니다.

LOSTARK_API_TOKEN=<본인 api 키>


#### 5. 데이터베이스 마이그레이션

python manage.py migrate


#### 6. 실행

python manage.py runserver


## 참고 자료

#### 로스트아크 공식 api : https://developer-lostark.game.onstove.com/

