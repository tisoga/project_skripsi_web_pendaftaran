from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('page_siswa.urls')),
    path('admin/', include('page_admin.urls')),
    path('api/', include('api.urls')),
    # path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
