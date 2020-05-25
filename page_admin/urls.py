from django.urls import path, include
from . import views
from . import ajax
from page_siswa.views import redirect_sites
app_name = 'admin_page'

urlpatterns = [
    path('', redirect_sites, name='rd'),
    path('home/', views.homepage, name='home'),
    path('list_siswa/', views.listsiswa, name='list_siswa'),
    path('verifikasi_siswa/', views.verifikasi_siswa, name='verifikasi_siswa'),
    path('events/', views.events, name='events'),
    path('ajax/list_siswa', ajax.list_siswa, name='ajax_list_siswa'),
]