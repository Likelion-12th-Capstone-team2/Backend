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
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        # URL로 크롤링 수행
        response = requests.get(url, headers=headers)
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

        # 이미지 다운로드
        image_content = None
        if product_image_url:
            image_response = requests.get(product_image_url)
            if image_response.status_code == 200:
                image_content = ContentFile(
                    image_response.content, name=f"{product_name}.jpg")

        # 카테고리 생성 또는 가져오기
        category_name = 'Default'
        category, created = Category.objects.get_or_create(
            user=request.user,
            category=category_name  # 올바른 필드명 사용
        )

        # Wish 모델에 저장
        wish = Wish.objects.create(
            user=request.user,
            item_name=product_name,
            price=int(product_price),
            item_image=image_content if image_content else None,
            wish_link=url,
            category=category,  # ForeignKey에 객체 전달
            heart=0  # 초기값
        )

        return Response({
            'message': 'Product crawled and saved successfully',
            'wish_id': wish.id,
            'product_name': product_name,
            'product_price': product_price,
            'product_image': product_image_url
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
