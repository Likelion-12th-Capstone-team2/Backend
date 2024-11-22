from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from wish.models import Wish
from mypage.models import Category

@csrf_exempt
def crawl_product(request):
    if request.method == 'POST':
        try:
            # 요청에서 URL 받기
            data = json.loads(request.body)
            url = data.get('url')

            # 크롤링할 웹페이지 가져오기
            response = requests.get(url)
            response.raise_for_status()

            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 필요한 데이터 추출 (예: 상품명, 가격, 이미지)
            product_name = soup.select_one('.product-name').get_text()  # 예시 클래스명
            product_price = soup.select_one('.product-price').get_text()  # 예시 클래스명
            product_image = soup.select_one('.product-image img')['src']  # 이미지 URL

            # 로그인된 사용자 가져오기
            if not request.user.is_authenticated:
                return JsonResponse({'error': '로그인 후 사용할 수 있습니다.'}, status=400)

            user = request.user

            # 카테고리 처리
            category_name = 'Default'  # 기본 카테고리 (원하는 카테고리로 수정 가능)
            category, created = Category.objects.get_or_create(user=user, category=category_name)

            # 크롤링된 데이터를 Wish 모델에 저장
            wish = Wish.objects.create(
                user=user,
                item_name=product_name,
                price=product_price,
                item_image=product_image,
                category=category,
                heart=0,  # 초기값 설정
                wish_link=url  # 크롤링된 URL을 저장
            )

            # 데이터 반환
            return JsonResponse({
                'product_name': product_name,
                'product_price': product_price,
                'product_image': product_image,
                'wish_id': wish.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=400)