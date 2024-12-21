from rest_framework.decorators import api_view
from rest_framework.response import Response
from wish.models import Wish
from mypage.models import Category
from django.core.files.base import ContentFile
from rest_framework import status
import requests
from bs4 import BeautifulSoup


@api_view(['POST'])
def crawl_and_save_product(request):
    try:
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=400)

        # 유저 인증 확인
        if request.user.is_anonymous:
            return Response({'error': 'User must be authenticated'}, status=400)

        # 크롤링 수행
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name = soup.select_one('.product-title')
        product_name = product_name.get_text(
            strip=True) if product_name else 'Unknown Product'

        product_price = soup.select_one('.total-price')
        product_price = product_price.get_text(strip=True).replace(
            ',', '').replace('₩', '') if product_price else '0'

        product_image = soup.select_one('.prod-image img')
        product_image_url = product_image['src'] if product_image else None

        # 카테고리 생성 또는 가져오기
        category, created = Category.objects.get_or_create(
            user=request.user,  # ForeignKey 필드
            category="Default"
        )

        # Wish 모델에 저장
        wish = Wish.objects.create(
            user=request.user,
            item_name=product_name,
            price=int(product_price),
            item_image=None,  # 이미지 업로드 처리
            wish_link=url,
            category=category,
            heart=0  # 초기값
        )

        return Response({
            'product_name': product_name,
            'product_price': product_price,
            'product_image': product_image_url,
        }, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=400)
