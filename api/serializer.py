from rest_framework import serializers
from page_siswa.models import Siswa, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','first_name','last_name')

class ListSiswaSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Siswa
        fields = '__all__'