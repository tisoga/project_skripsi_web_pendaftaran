from django.urls import path
from . import views

app_name = 'siswa'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.login_views, name='login'),
    path('register/', views.register_views, name='register'),
    path('tahapan_pendaftaran/', views.tahapan_pendaftaran_views, name='tahapan_pendaftaran'),
    path('proses_pengajuan_pendaftaran', views.proses_ajukan_pendaftaran, name='proses_pengajuan'),
    path('success', views.success, name='success')
]