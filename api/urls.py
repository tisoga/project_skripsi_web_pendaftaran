from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('siswa/<int:nis>', views.ProfileAPI, name='profileAPI')
]