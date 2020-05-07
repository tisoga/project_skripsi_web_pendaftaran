from django.contrib import admin
from .models import CustomUser, Siswa, list_events
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Siswa)
admin.site.register(list_events)