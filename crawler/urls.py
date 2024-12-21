from django.urls import path
from crawler import views

app_name = 'crawler'


urlpatterns = [
    path('crawl/', views.crawl_product, name='crawl_product'),
]
