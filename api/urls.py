from django.urls import path, include
from knox import views as knox_views
from . import views

app_name = 'api'

urlpatterns = [
    path('auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('auth/login/', views.LoginAPI, name='login'),
    path('auth/register/', views.RegisterAPI, name='register'),
    path('profile/', views.ProfileSiswaAPI, name='profile'),
    path('profile/berkas/', views.UploadBerkasAPI),
    path('list_events/', views.ListKegiatanAPI, name='event'),
    path('notifikasi/', views.NotifikasiAPI, name='notifikasi'),
    path('siswa/<int:nis>', views.ProfileAPI, name='profileAPI'),
]