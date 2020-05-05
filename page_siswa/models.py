from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
# Create your models here


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email Harus di isi')
        elif not password:
            raise ValueError('Password Harus di isi')
        # print(extra_fields['first_name'])
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email Harus di isi')
        if not password:
            raise ValueError('Password Harus di isi')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class SiswaManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        email = self.normalize_email(email)
        email = CustomUser.object.create_user(
            email, password, first_name=first_name, last_name=last_name)
        user = self.model(user=email, **extra_fields)
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    object = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def DetailUser(self):
        user = CustomUser.object.get(email=self.email)
        detail = user.siswa
        return detail


class Siswa(models.Model):
    user = models.OneToOneField(
        CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='siswa')
    nis = models.CharField(max_length=20, default=None, null=True)
    jenis_kelamin = models.CharField(max_length=10, default=None, null=True)
    tanggal_lahir = models.DateField(default=None, null=True)
    tempat_lahir = models.CharField(max_length=255, default=None, null=True)
    umur = models.IntegerField(default=None, null=True)
    alamat = models.TextField(default=None, null=True)
    asal_sekolah = models.CharField(max_length=255, default=None, null=True)
    status = models.PositiveSmallIntegerField(default=0, null=True)
    nilai_matematika = models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2)
    nilai_indonesia = models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2)
    nilai_inggris = models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2)
    nilai_ipa = models.DecimalField(default=None, null=True, max_digits=4, decimal_places=2)
    foto_diri = models.ImageField(upload_to='images/', null=True, default=None)
    berkas_ijazah = models.ImageField(upload_to='images/', null=True, default=None)
    berkas_akta = models.ImageField(upload_to='images/', null=True, default=None)
    berkas_kesehatan = models.ImageField(upload_to='images/', null=True, default=None)

    object = SiswaManager()

    class Meta:
        db_table = 'tabel_siswa'

    def __str__(self):
        return self.user.get_full_name()

    def check_progress(self):
        if not (self.jenis_kelamin and self.tanggal_lahir and self.tempat_lahir \
            and self.umur and self.alamat and self.foto_diri) and \
                (self.jenis_kelamin and self.tanggal_lahir and self.tempat_lahir \
                    and self.umur and self.alamat and self.foto_diri):
            return '1'
        elif not (self.berkas_ijazah and self.berkas_akta and self.berkas_kesehatan \
            and self.nilai_indonesia and self.nilai_inggris and self.nilai_matematika and self.nilai_ipa) and \
                (self.berkas_ijazah and self.berkas_akta and self.berkas_kesehatan \
                    and self.nilai_indonesia and self.nilai_inggris and self.nilai_matematika and self.nilai_ipa):
            return '2'
        else:
            return '3'
    
    def print_status(self):
        if self.status == 0:
            color = 'text-secondary'
            text = 'Pelengkapan Identitas Diri'
        elif self.status == 1:
            color = 'text-secondary'
            text = 'Pelengkapan Berkas-Berkas'
        elif self.status == 2:
            color = 'text-secondary'
            text = 'Pengajuan Pendaftaran'
        elif self.status == 3:
            color = 'text-primary'
            text = 'Sedang Diverifikasi'
        elif self.status == 4:
            color = 'text-warning'
            text = 'Verifikasi Gagal'
        elif self.status == 5:
            color = 'text-primary'
            text = 'Proses Daftar Ulang'
        html = '<b>Status Pendaftaran :</b> <a class="{} float-right">{}</a>'.format(color, text)
        return html