from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('mypages/', include('mypage.urls')),
    path('wish/', include('wish.urls')),
    path('alarms/', include('alarms.urls')),
    path('crawler/', include('crawler.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# "99"