from django.urls import path
from . import views

urlpatterns = [
    path('crawl/', views.crawl_product, name='crawl_product'),
]