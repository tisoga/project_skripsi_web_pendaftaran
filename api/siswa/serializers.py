from rest_framework import serializers
from django.contrib.auth import authenticate
from page_siswa.models import CustomUser, Siswa


class DetailUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Siswa
        exclude = ('user',)
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    DetailUser = DetailUserSerializer(read_only=True, many=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'DetailUser')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError(
            'Cek Kembali Email dan Password Anda')


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Siswa.object.create_user(
            validated_data['email'], validated_data['password'], 
            validated_data['first_name'], validated_data['last_name'])
        user.email = user.user.email
        user.first_name = user.user.first_name
        user.last_name = user.user.last_name

        return user
