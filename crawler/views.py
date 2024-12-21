from rest_framework.decorators import api_view
from rest_framework.response import Response
from wish.models import Wish
from mypage.models import Category
import requests
from bs4 import BeautifulSoup
from rest_framework import status


@api_view(['GET', 'POST'])  # GET 요청 추가
def crawl_product(request):
    if request.method == 'GET':
        # 예: 단순한 응답 반환
        return Response({'message': 'This is a GET request endpoint'}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            # 요청에서 URL 받기
            url = request.data.get('url')
            if not url:
                return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

            # 크롤링할 웹페이지 가져오기
            response = requests.get(url)
            response.raise_for_status()

            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 필요한 데이터 추출 (예: 상품명, 가격, 이미지)
            product_name = soup.select_one(
                '.product-name').get_text()  # 예시 클래스명
            product_price = soup.select_one(
                '.product-price').get_text()  # 예시 클래스명
            product_image = soup.select_one(
                '.product-image img')['src']  # 이미지 URL

            # 기본 카테고리 처리
            category_name = 'Default'
            category, created = Category.objects.get_or_create(
                user=request.user, name=category_name  # 수정: 필드명 점검
            )

            # Wish 모델에 크롤링된 데이터 저장
            wish = Wish.objects.create(
                user=request.user,
                item_name=product_name,
                price=product_price,
                item_image=product_image,
                category=category,
                heart=0,
                wish_link=url
            )

            # 성공적인 응답 반환
            return Response({
                'product_name': product_name,
                'product_price': product_price,
                'product_image': product_image,
                'wish_id': wish.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 허용되지 않은 요청 메서드 처리 (기본적으로 여기까지 도달하지 않음)
    return Response({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
