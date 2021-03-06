import json
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def create_admin(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email Harus di isi')
        elif not password:
            raise ValueError('Password Harus di isi')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)

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
        try:
            nis = int(Siswa.object.latest('nis').nis) + 1
        except ObjectDoesNotExist:
            nis = '2021001'
        print(nis)
        user = self.model(user=email, nis=nis, **extra_fields)
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

    class Meta:
        db_table = 'tabel_user'

    object = CustomUserManager()
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def DetailUser(self):
        user = CustomUser.object.get(email=self.email)
        detail = user.siswa
        return detail


def ijazah_image_path(instance, filename):
    return 'images/{0}/file_ijazah.jpg'.format(instance.nis)


def akta_image_path(instance, filename):
    return 'images/{0}/file_akta.jpg'.format(instance.nis)


def kesehatan_image_path(instance, filename):
    return 'images/{0}/file_kesehatan.jpg'.format(instance.nis)


def tambahan_image_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.nis, filename)


def foto_image_path(instance, filename):
    return 'images/{0}/foto_diri.jpg'.format(instance.nis)


class Siswa(models.Model):

    class JenisKelamin(models.TextChoices):
        laki_laki = 'L', _('Laki-Laki')
        perempuan = 'P', _('Perempuan')

    class StatusPendaftaran(models.IntegerChoices):
        identitas = 0, _('Pelengkapan Identias Diri')
        berkas = 1, _('Pelengkapan Berkas-Berkas')
        pengajuan = 2, _('Pengajuan Pendaftaran')
        verifikasi = 3, _('Sedang Diverifikasi')
        gagal = 4, _('Verifikasi Gagal')
        daftar_ulang = 5, _('Proses Daftar Ulang')
        seleksi = 6, _('Proses Seleksi Siswa')
        tidak = 7, _('Tidak Diterima')
        diterima = 8, _('Diterima')
        tutup = 9, _('Pendaftaran ditutup')
        zonasi = 10, _('Jalur Zonasi')
        afirmasi = 11, _('Jalur Afirmasi')
        perpindahan = 12, _('Jalur Perpindahan')
        prestasi = 13, _('Jalur Prestasi')

    user = models.OneToOneField(
        CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='siswa')
    nis = models.CharField(max_length=20, default=None, null=True)
    jenis_kelamin = models.CharField(
        max_length=1,
        choices=JenisKelamin.choices,
        default=None,
        null=True)
    tanggal_lahir = models.DateField(default=None, null=True)
    tempat_lahir = models.CharField(max_length=255, default=None, null=True)
    umur = models.IntegerField(default=None, null=True)
    alamat = models.TextField(default=None, null=True)
    jalur_pendaftaran = models.CharField(max_length=255, default=None, null=True)
    status = models.IntegerField(
        choices=StatusPendaftaran.choices, null=True, default=0)
    nilai_matematika = models.DecimalField(
        default=None, null=True, max_digits=5, decimal_places=2, validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    nilai_indonesia = models.DecimalField(
        default=None, null=True, max_digits=5, decimal_places=2, validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    nilai_inggris = models.DecimalField(
        default=None, null=True, max_digits=5, decimal_places=2, validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    nilai_ipa = models.DecimalField(
        default=None, null=True, max_digits=5, decimal_places=2, validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ])
    foto_diri = models.ImageField(
        upload_to=foto_image_path, null=True, default=None)
    berkas_ijazah = models.ImageField(
        upload_to=ijazah_image_path, null=True, default=None)
    berkas_akta = models.ImageField(
        upload_to=akta_image_path, null=True, default=None)
    berkas_kesehatan = models.ImageField(
        upload_to=kesehatan_image_path, null=True, default=None)
    berkas_tambahan = models.ImageField(
        upload_to=tambahan_image_path, null=True, default=None)

    object = SiswaManager()

    class Meta:
        db_table = 'tabel_siswa'
        ordering = ['nis']

    def __str__(self):
        return self.nis

    def get_kabupaten_siswa(self):
        data = self.alamat
        data = data.split(',')
        print(data)
        return data[3].strip()

    def get_kecamatan_siswa(self):
        data = self.alamat
        data = data.split(',')
        return data[2].strip()

    def get_desa_siswa(self):
        data = self.alamat
        data = data.split(',')
        return data[1].strip()

    def check_progress(self):
        if not (self.jenis_kelamin and self.tanggal_lahir and self.tempat_lahir
                and self.umur and self.alamat and self.foto_diri) and \
                (self.jenis_kelamin and self.tanggal_lahir and self.tempat_lahir
                    and self.umur and self.alamat and self.foto_diri):
            return '1'
        elif not (self.berkas_ijazah and self.berkas_akta and self.berkas_kesehatan
                  and self.nilai_indonesia and self.nilai_inggris and self.nilai_matematika and self.nilai_ipa) and \
                (self.berkas_ijazah and self.berkas_akta and self.berkas_kesehatan
                    and self.nilai_indonesia and self.nilai_inggris and self.nilai_matematika and self.nilai_ipa):
            return '2'
        else:
            return '3'

    def check_rata_rata(self):
        if self.nilai_indonesia and self.nilai_inggris and self.nilai_ipa and self.nilai_matematika:
            rata_rata = (self.nilai_indonesia + self.nilai_inggris +
                         self.nilai_ipa + self.nilai_matematika) / 4
            return round(rata_rata, 2)
        else:
            return None

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
            color = 'text-danger'
            text = 'Verifikasi Gagal'
        elif self.status == 5:
            color = 'text-primary'
            text = 'Proses Daftar Ulang'
        elif self.status == 6 or self.status == 10 or self.status == 11 or self.status == 12 or self.status == 13:
            color = 'text-primary'
            text = 'Proses Seleksi Siswa'
        elif self.status == 7:
            color = 'text-danger'
            text = 'Tidak Diterima'
        elif self.status == 8:
            color = 'text-success'
            text = 'Diterima'
        elif self.status == 9:
            color = 'text-secondary'
            text = 'Pendaftaran ditutup'
        html = '<b>Status Pendaftaran :</b> <a class="{} float-right">{}</a>'.format(
            color, text)
        data = {
            'html': html,
            'status': text
        }
        return data


class list_events(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None,  blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tabel_events'


class list_notifikasi(models.Model):
    siswa = models.ForeignKey(
        Siswa, on_delete=models.CASCADE, related_name='notifikasi', default=None)
    notifikasi = models.CharField(max_length=255)
    tanggal_notifikasi = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.tanggal_notifikasi)

    class Meta:
        db_table = 'tabel_notifikasi'
        ordering = ['-tanggal_notifikasi', '-id']


class sekolah(models.Model):

    class StatusPendaftaran(models.IntegerChoices):
        tutup = 0, _('Pendaftaran ditutup')
        buka = 1, _('Pendaftaran dibuka')
        seleksi = 2, _('Proses Seleksi')
        ulang = 3, _('Proses Daftar Ulang')
        pengumuman = 4, _('Pengumuman')

    nama = models.CharField(max_length=255, default=None)
    alamat = models.TextField(default=None)
    alamat_lengkap = models.TextField(default=None, null=True)
    daya_tampung = models.PositiveIntegerField(default=0)
    sisa_zonasi = models.PositiveIntegerField(default=0)
    sisa_afirmasi = models.PositiveIntegerField(default=0)
    sisa_perpindahan = models.PositiveIntegerField(default=0)
    sisa_prestasi = models.PositiveIntegerField(default=0)
    status_pendaftaran = models.IntegerField(
        choices=StatusPendaftaran.choices, default=1)
    jam_daftar_ulang = models.TextField(default=None, null=True)
    tanggal_daftar_ulang = models.TextField(default=None, null=True)

    class Meta:
        db_table = 'tabel_sekolah'

    def __str__(self):
        return self.nama

    def pembagian_kuota(self):
        jumlah_siswa = self.daya_tampung

        zonasi = int(self.daya_tampung * 0.50)
        afirmasi = int(self.daya_tampung * 0.15)
        perpindahan = int(self.daya_tampung * 0.05)
        prestasi = int(self.daya_tampung * 0.30)
        sisa = jumlah_siswa - (zonasi + afirmasi + perpindahan + prestasi)

        data = {'zonasi': zonasi, 'afirmasi': afirmasi,
                'perpindahan': perpindahan, 'prestasi': prestasi+sisa}
        return json.dumps(data)

    def split_alamat(self):
        data = {}
        alamat_str = self.alamat
        alamat_list = alamat_str.split(',')
        # print(alamat_str)
        # print(alamat_list)
        for cut in alamat_list:
            alamat = cut.split(':')
            data[alamat[0].strip()] = alamat[1].strip()
        return json.dumps(data)

    def split_tanggal_jam(self):
        data = {}
        tanggal_str = self.tanggal_daftar_ulang
        jam_str = self.jam_daftar_ulang
        tanggal_list = tanggal_str.split(',')
        jam_list = jam_str.split(',')
        data['tgl_mulai'] = tanggal_list[0]
        data['tgl_akhir'] = tanggal_list[1]
        data['jam_mulai'] = jam_list[0]
        data['jam_akhir'] = jam_list[1]
        return data
