from django.urls import path
from . import views
from . import ajax
from page_admin import ajax as ajax_admin
app_name = 'siswa'

urlpatterns = [
    path('', views.redirect_sites, name='rd'),
    path('home/', views.homepage, name='home'),
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('register/', views.register_views, name='register'),
    path('tahapan_pendaftaran/', views.tahapan_pendaftaran_views, name='tahapan_pendaftaran'),
    path('proses_pengajuan_pendaftaran', views.proses_ajukan_pendaftaran, name='proses_pengajuan'),
    path('pengumuman/', views.pengumuman_penerimaan, name='pengumuman'),
    path('success', views.success, name='success'),
    path('ajax/get_provinsi', ajax.get_provinsi, name='ajax_provinsi'),
    path('ajax/get_kota/<int:id>', ajax.get_kota, name='ajax_kota'),
    path('ajax/get_kecamatan/<int:id>', ajax.get_kecamatan, name='ajax_kecamatan'),
    path('ajax/get_kelurahan/<int:id>', ajax.get_kelurahan, name='ajax_kelurahan'),
]