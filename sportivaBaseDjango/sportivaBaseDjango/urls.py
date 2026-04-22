from django.contrib import admin
from django.urls import path, include # Додај include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('DjangoSportivaBase.urls')), # Го поврзуваме со апликацијата
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)