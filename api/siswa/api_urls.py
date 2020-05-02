from django.urls import path
from knox.urls import views as knox_views
from api.siswa import api_views

urlpatterns = [
    path('auth/login', api_views.loginAPI, name='login'),
    path('auth/register', api_views.RegisterAPI, name='register'),
    path('auth/user', api_views.UserAPI, name='user'),
    path('auth/logout', knox_views.LogoutView.as_view(), name='logout'),
]