from django.urls import path
from crawler import views

app_name = 'crawler'

urlpatterns = [
    path('crawl/', views.crawl_product, name='crawl_product'),  # 'crawl_product'라는 이름으로 URL을 설정
]