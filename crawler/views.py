from rest_framework.decorators import api_view
from rest_framework.response import Response
from wish.models import Wish
from mypage.models import Category
from django.core.files.base import ContentFile
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .seleniumCrawl import fetch_product_data

@api_view(['POST'])
def crawl_product(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required'}, status=400)

    # Selenium 크롤링 함수 호출
    product_data = fetch_product_data(url)

    if 'error' in product_data:
        return Response({'error': product_data['error']}, status=404)

    return Response(product_data, status=200)

