from django.contrib.auth import authenticate
from rest_framework import serializers
from page_siswa.models import Siswa, CustomUser, list_events, list_notifikasi
from page_siswa.functions import CompressImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class ListSiswaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Siswa
        fields = '__all__'

    def update(self, instance, validated_data):
        # if instance.user.DetailUser.status != 0:
        #     raise serializers.ValidationError(
        #         'Terjadi Kesalahan, Silahkan Coba Lagi!')
        # validated_data['status'] = 1
        user = CustomUser.object.get(pk=instance.user.id)
        if 'first_name' in validated_data:
            first_name = validated_data.pop('first_name')
            user.first_name = first_name
            instance.user.first_name = first_name
        if 'last_name' in validated_data:
            last_name = validated_data.pop('last_name')
            user.last_name = last_name
            instance.user.last_name = last_name
        instance.__dict__.update(**validated_data)
        user.save()
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_staff:
            return user
        raise serializers.ValidationError(
            'Cek Kembali Email dan Password anda!')


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Siswa.object.create_user(
            email=validated_data['email'], password=validated_data['password'],
            first_name=validated_data['first_name'], last_name=validated_data['last_name'])

        return user


class PelengkapanIdentitasSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Siswa
        fields = ('user', 'first_name', 'last_name', 'nis', 'jenis_kelamin', 'tanggal_lahir',
                  'tempat_lahir', 'umur', 'alamat', 'foto_diri', 'status')
        read_only_fields = ['nis']
        extra_kwargs = {
            'jenis_kelamin': {'required': True},
            'tanggal_lahir': {'required': True},
            'tempat_lahir': {'required': True},
            'umur': {'required': True},
            'alamat': {'required': True},
            'foto_diri': {'required': True}}

    def update(self, instance, validated_data):
        if instance.user.DetailUser.status != 0:
            raise serializers.ValidationError(
                'Terjadi Kesalahan, Silahkan Coba Lagi!')
        validated_data['status'] = 1
        validated_data['foto_diri'] = CompressImage(
            validated_data.pop('foto_diri'))
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = CustomUser.object.get(pk=instance.user.id)
        user.first_name = first_name
        user.last_name = last_name
        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.__dict__.update(**validated_data)
        user.save()
        instance.save()
        return instance


class PelengkapanBerkasSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Siswa
        fields = ['user', 'nis', 'berkas_ijazah', 'berkas_akta', 'berkas_kesehatan',
                  'nilai_indonesia', 'nilai_ipa', 'nilai_inggris', 'nilai_matematika', 'status',
                  'jenis_kelamin', 'tanggal_lahir', 'foto_diri']
        read_only_fields = ['nis', 'status', 'status',
                            'jenis_kelamin', 'tanggal_lahir', 'foto_diri']
        extra_kwargs = {
            'berkas_ijazah': {'required': True},
            'berkas_akta': {'required': True},
            'berkas_kesehatan': {'required': True},
            'nilai_ipa': {'required': True},
            'nilai_indonesia': {'required': True},
            'nilai_matematika': {'required': True},
            'nilai_inggris': {'required': True},
        }

    def update(self, instance, validated_data):
        if instance.user.DetailUser.status != 1:
            raise serializers.ValidationError(
                'Terjadi Kesalahan, Silahkan Coba Lagi!')
        validated_data['status'] = 2
        validated_data['berkas_ijazah'] = CompressImage(
            validated_data.pop('berkas_ijazah'))
        validated_data['berkas_akta'] = CompressImage(
            validated_data.pop('berkas_akta'))
        validated_data['berkas_kesehatan'] = CompressImage(
            validated_data.pop('berkas_kesehatan'))
        instance.__dict__.update(**validated_data)
        instance.save()

        return instance


class PengajuanPendaftaranSerializer(serializers.ModelSerializer):

    class Meta:
        model = Siswa
        fields = ['nis', 'status','berkas_tambahan']
        read_only_fields = ['nis']
        extra_kwargs = {'status': {'required': True}}

    def update(self, instance, validated_data):
        if instance.user.DetailUser.status != 2:
            raise serializers.ValidationError(
                'Terjadi Kesalahan, Silahkan Coba Lagi!')
        instance.status = validated_data['status']
        instance.save()

        return instance


class EditPengajuanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Siswa
        fields = ('user', 'first_name', 'last_name', 'nis', 'jenis_kelamin', 'tanggal_lahir',
                  'tempat_lahir', 'umur', 'alamat', 'status', 'nilai_matematika',
                  'nilai_inggris', 'nilai_ipa', 'nilai_indonesia', 'foto_diri', 'berkas_akta',
                  'berkas_kesehatan', 'berkas_ijazah')
        read_only_fields = ['nis']

    def update(self, instance, validated_data):
        if instance.user.DetailUser.status != 2:
            raise serializers.ValidationError(
                'Terjadi Kesalahan, Silahkan Coba Lagi!')
        user = CustomUser.object.get(pk=instance.user.id)
        if validated_data.get('first_name'):
            first_name = validated_data.pop('first_name')
            last_name = validated_data.pop('last_name')
            user.first_name = first_name
            user.last_name = last_name
            instance.user.first_name = first_name
            instance.user.last_name = last_name
        if validated_data.get('foto_diri'):
            validated_data['foto_diri'] = CompressImage(
                validated_data.pop('foto_diri'))
        if validated_data.get('berkas_ijazah'):
            validated_data['berkas_ijazah'] = CompressImage(
                validated_data.pop('berkas_ijazah'))
        if validated_data.get('berkas_akta'):
            validated_data['berkas_akta'] = CompressImage(
                validated_data.pop('berkas_akta'))
        if validated_data.get('berkas_kesehatan'):
            validated_data['berkas_kesehatan'] = CompressImage(
                validated_data.pop('berkas_kesehatan'))
        instance.__dict__.update(**validated_data)
        user.save()
        instance.save()
        return instance


class KegiatanSerializer(serializers.ModelSerializer):

    class Meta:
        model = list_events
        fields = '__all__'


class NotifikasiSerializer(serializers.ModelSerializer):

    class Meta:
        model = list_notifikasi
        fields = ['id', 'notifikasi', 'tanggal_notifikasi']
