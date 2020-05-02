from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('siswa/', include('api.siswa.api_urls'))
]