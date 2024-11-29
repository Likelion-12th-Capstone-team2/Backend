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
<<<<<<< HEAD
    path('alarms/', include('alarms.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

=======
    path('crawler/', include('crawler.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
>>>>>>> 574b800fcdf6d1fa7d7504dc8fb5e287469603ce
