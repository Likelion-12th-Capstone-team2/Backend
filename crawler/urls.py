from django.urls import path
from crawler import views

app_name = 'crawler'

urlpatterns = [
    path('crawl/', views.crawl_and_save_product, name='crawl_and_save_product'),  # POST 요청 처리
]
