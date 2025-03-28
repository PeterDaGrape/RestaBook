from django.contrib import admin
from django.urls import path
from django.urls import include
from app import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('app/', include('app.urls')),
    # The above maps any URLs starting with rango/ to be handled by rango.
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)