import requests
import json
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from page_siswa.functions import CompressImage, convert_date
from .models import CustomUser, Siswa, list_events, list_notifikasi, sekolah

# Create your views here.


def login_views(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    if request.method == 'POST':
        if request.POST.get('email'):
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user and user.is_staff:
                login(request, user)
                return redirect('admin_page:home')
            elif user and not user.is_staff:
                login(request, user)
                return redirect('siswa:home')
            else:
                messages.error(
                    request, f'Cek Kembali Email atau Password anda')
                return redirect('siswa:login')
    return render(request=request,
                  template_name='page_siswa/login.html',
                  context={'data_sekolah': data_sekolah})


def logout_views(request):
    logout(request)
    return redirect('siswa:login')


def register_views(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    if request.method == 'POST':
        if request.POST.get('email'):
            if request.POST['pass'] != request.POST['pass2']:
                messages.error(request, 'Kesalahan : Password Tidak Sama')
                return redirect('siswa:register')
            email = request.POST['email']
            first = request.POST['first']
            last = request.POST['last']
            password = request.POST['pass']
            try:
                Siswa.object.create_user(email, password, first, last)
                messages.success(request, 'Register Berhasil, Silahkan Login')
                return redirect('siswa:login')
            except IntegrityError:
                messages.error(request, 'Kesalahan : Email Sudah Terdaftar')
    return render(request=request,
                  template_name='page_siswa/register.html',
                  context={'data_sekolah': data_sekolah})


def redirect_sites(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    else:
        return redirect('siswa:login')


def homepage(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif not request.user.is_authenticated:
        return redirect('siswa:login')
    # print(request.user.DetailUser.get_jenis_kelamin_display())
    page = 'home'
    events = list_events.objects.all()
    notifikasi = list_notifikasi.objects.filter(siswa=request.user.id)
    if request.method == 'POST':
        if request.POST.get('email'):
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            Siswa.object.create_user(
                email=email, password=password, first_name=first_name, last_name=last_name)
            return redirect('siswa:login')
    return render(request=request,
                  template_name='page_siswa/home.html',
                  context={'page': page, 'events': events, 'notifikasi': notifikasi})


def tahapan_pendaftaran_views(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif not request.user.is_authenticated:
        return redirect('siswa:login')
    data_sekolah = sekolah.objects.first()
    data = Siswa.object.get(user=request.user)
    status = data.status
    # print(data_sekolah.status_pendaftaran)
    # print(status)
    if data_sekolah.status_pendaftaran == 1:
        if status == 0:
            page = 'Identitas Diri'
        elif status == 1:
            page = 'Berkas-Berkas'
        elif status == 2 or status == 4:
            page = 'Pengajuan Pendaftaran'
        elif status == 3 or status == 6 or status == 7 or status == 8 or status == 9 or status == 10 or status == 11 or status == 12 or status == 13:
            # page = 'Pengajuan Pendaftaran'
            # print('why')
            return redirect('siswa:home')
        elif status == 5:
            data_sekolah.lengkap = json.loads(data_sekolah.split_alamat())
            page = 'Daftar Ulang'
    elif data_sekolah.status_pendaftaran == 3:
        if status == 5:
            page = 'Daftar Ulang'
    else:
        messages.error(
            request, f'Pendaftaran sudah ditutup, anda tidak bisa lagi untuk mengajukan pendaftaran!')
        return redirect('siswa:home')
    # print(page)
    if request.method == 'POST':
        if request.POST.get('first_name'):
            if request.user.DetailUser.status != 0:
                messages.error(request, f'Terjadi Kesalahn')
                return redirect('siswa:home')
            if int(request.POST.get('umur')) > 21:
                messages.error(
                    request, f'Maaf Umur Anda Sudah Melebihi Batas Maksimal untuk Melakukan PPDB tingkat SMA. Batas Umur Maksimal melakukan PPDB Tingkat SMA Adalah 21 Tahun')
                return redirect('siswa:tahapan_pendaftaran')
            lengkap = request.POST.get('alamat')
            provinsi = request.POST.get('prov')
            kabupaten = request.POST.get('kab')
            kecamatan = request.POST.get('kec')
            desa = request.POST.get('desa')
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            data.jenis_kelamin = request.POST.get('jk')
            data.tanggal_lahir = convert_date(request.POST.get('tanggal'))
            data.tempat_lahir = request.POST.get('tempat')
            data.status = 1
            data.umur = request.POST.get('umur')
            data.alamat = '{}, {}, {}, {}, {}'.format(
                lengkap, desa, kecamatan, kabupaten, provinsi)
            # data.foto_diri = CompressImage(request.FILES.get('foto'))
            data.foto_diri = request.FILES.get('foto')
            data.save()
            messages.success(request, f'Identitas Diri Berhasil disimpan')
            return redirect('siswa:home')
        elif request.POST.get('mtk'):
            if request.user.DetailUser.status != 1:
                messages.error(request, f'Terjadi Kesalahn')
                return redirect('siswa:home')
            data.nilai_matematika = request.POST.get('mtk')
            data.nilai_indonesia = request.POST.get('indo')
            data.nilai_inggris = request.POST.get('ing')
            data.nilai_ipa = request.POST.get('ipa')
            data.status = 2
            # data.berkas_ijazah = CompressImage(request.FILES.get('skhun'))
            # data.berkas_akta = CompressImage(request.FILES.get('akta'))
            # data.berkas_kesehatan = CompressImage(
            #     request.FILES.get('kesehatan'))
            data.berkas_ijazah = request.FILES.get('skhun')
            data.berkas_akta = request.FILES.get('akta')
            data.berkas_kesehatan = request.FILES.get('kesehatan')
            data.save()
            messages.success(request, f'Berkas-Berkas Berhasil disimpan')
            return redirect('siswa:home')
    return render(request=request,
                  template_name='page_siswa/tahapan_pendaftaran.html',
                  context={'page': page, 'sekolah': data_sekolah})


def proses_ajukan_pendaftaran(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif not request.user.is_authenticated:
        return redirect('siswa:login')
    if request.user.DetailUser.status != 2:
        messages.error(request, f'Terjadi Kesalahn')
        return redirect('siswa:home')
    if request.method == 'POST':
        data_siswa = Siswa.object.get(pk=request.user)
        if request.POST.get('decision') == 'edit':
            if int(request.POST.get('umur')) > 21:
                messages.error(
                    request, f'Maaf Umur Anda Sudah Melebihi Batas Maksimal untuk Melakukan PPDB tingkat SMA. Batas Umur Maksimal melakukan PPDB Tingkat SMA Adalah 21 Tahun')
                return redirect('siswa:tahapan_pendaftaran')
            lengkap = request.POST.get('alamat')
            provinsi = request.POST.get('prov')
            kabupaten = request.POST.get('kab')
            kecamatan = request.POST.get('kec')
            desa = request.POST.get('desa')
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            data_siswa.jenis_kelamin = request.POST.get('jk')
            data_siswa.tanggal_lahir = convert_date(
                request.POST.get('tanggal'))
            data_siswa.tempat_lahir = request.POST.get('tempat')
            data_siswa.umur = request.POST.get('umur')
            data_siswa.nilai_matematika = request.POST.get('mtk')
            data_siswa.nilai_indonesia = request.POST.get('indo')
            data_siswa.nilai_inggris = request.POST.get('ing')
            data_siswa.nilai_ipa = request.POST.get('ipa')
            if lengkap and provinsi and kabupaten and kecamatan and desa:
                data_siswa.alamat = '{}, {}, {}, {}, {}'.format(
                    lengkap, desa, kecamatan, kabupaten, provinsi)
            if request.FILES.get('foto'):
                foto = request.FILES.get('foto')
                # foto = CompressImage(request.FILES.get('foto'))
                data_siswa.foto_diri = foto
            if request.FILES.get('skhun'):
                ijazah = request.FILES.get('skhun')
                # ijazah = CompressImage(request.FILES.get('skhun'))
                data_siswa.berkas_ijazah = ijazah
            if request.FILES.get('akta'):
                akta = request.FILES.get('akta')
                # akta = CompressImage(request.FILES.get('akta'))
                data_siswa.berkas_akta = akta
            if request.FILES.get('kesehatan'):
                kesehatan = request.FILES.get('kesehatan')
                data_siswa.berkas_kesehatan = kesehatan
            # print(request.POST)
            request.user.save()
            data_siswa.save()
            messages.success(request, f'Identitas Diri Berhasil diedit')
            return redirect('siswa:tahapan_pendaftaran')
        else:
            print(request.FILES)
            if request.POST.get('pengajuan') == 'zonasi':
                check = json.loads(sekolah.objects.first().split_alamat())
                if check['kabupaten'] != data_siswa.get_kabupaten_siswa():
                    messages.error(request, f'Terjadi Kesalahan')
                    return redirect('siswa:home')
                pengajuan = 10
                jalur = 'Zonasi'
                tambahan = None
            elif request.POST.get('pengajuan') == 'afirmasi':
                pengajuan = 11
                jalur = 'Afirmasi'
                # tambahan = CompressImage(
                #     request.FILES.get('afirmasi'), 'file_afirmasi')
                tambahan = request.FILES.get('afirmasi')
            elif request.POST.get('pengajuan') == 'perpindahan':
                pengajuan = 12
                jalur = 'Perpindahan OrangTua'
                tambahan = request.FILES.get('perpindahan')
            elif request.POST.get('pengajuan') == 'prestasi':
                pengajuan = 13
                jalur = 'Prestasi'
                if 'prestasi' in request.FILES:
                    tambahan = request.FILES.get('prestasi')
                else:
                    tambahan = None
            data_siswa.status = pengajuan
            data_siswa.jalur_pendaftaran = jalur
            data_siswa.berkas_tambahan = tambahan
            data_siswa.save()
            messages.success(
                request, f'Pengajuan Pendaftaran Berhasil, Silahkan Tunggu Proses Seleksi.')
            return redirect('siswa:home')


def pengumuman_penerimaan(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif not request.user.is_authenticated:
        return redirect('siswa:login')
    data_sekolah = sekolah.objects.first()
    lolos_zonasi = Siswa.object.filter(status=8).filter(jalur_pendaftaran='Zonasi').annotate(
        avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
    lolos_afirmasi = Siswa.object.filter(
        status=8).filter(jalur_pendaftaran='Afirmasi').annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
    lolos_perpindahan = Siswa.object.filter(
        status=8).filter(jalur_pendaftaran='Perpindahan').annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
    lolos_prestasi = Siswa.object.filter(
        status=8).filter(jalur_pendaftaran='Prestasi').annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
    data_siswa = {
        'lolos_zonasi': lolos_zonasi,
        'lolos_afirmasi': lolos_afirmasi,
        'lolos_perpindahan': lolos_perpindahan,
        'lolos_prestasi': lolos_prestasi,
    }
    # print(data_siswa)
    return render(request=request,
                  template_name='page_siswa/pengumuman_penerimaan.html',
                  context={'data_siswa': data_siswa, 'data_sekolah': data_sekolah})


def ganti_password(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_page:home')
    elif not request.user.is_authenticated:
        return redirect('siswa:login')
    return render(request=request,
                  template_name='page_siswa/ganti_password.html')

def informasi_pendaftaran(request):
    data_sekolah = sekolah.objects.first()
    alamat = json.loads(data_sekolah.split_alamat())
    daya_tampung = json.loads(data_sekolah.pembagian_kuota())
    data_sekolah.quota_jalur = daya_tampung
    data_sekolah.alamat_lengkap = f'{data_sekolah.alamat_lengkap}, {alamat["desa"]}, {alamat["kecamatan"]}, {alamat["kabupaten"]}, {alamat["provinsi"]}'
    # print(data_sekolah.alamat_lengkap)  
    return render(request = request,
                  template_name = 'page_siswa/informasi_pendaftaran.html',
                  context={'data_sekolah': data_sekolah})

def success(request):
    cs = CustomUser.object.get(email=request.user.email)
    if request.method == 'POST':
        siswa = request.user.siswa
        if request.POST.get('alamat'):
            siswa.alamat = request.POST['alamat']
            siswa.tanggal_lahir = request.POST['date']
            siswa.umur = request.POST['umur']
            siswa.jenis_kelamin = request.POST['jk']
            siswa.foto_diri = request.FILES['foto']
            siswa.save()
        elif request.POST.get('mtk'):
            siswa.nilai_un_matematika = request.POST['mtk']
            siswa.nilai_un_indonesia = request.POST['indo']
            siswa.nilai_un_inggris = request.POST['ing']
            siswa.foto_ijazah = request.FILES['skhun']
            siswa.save()
    return render(request=request,
                  template_name='page_siswa/test_success.html')