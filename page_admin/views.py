import json

from django.shortcuts import render, redirect
from django.db.models import F, Q, Avg
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from page_siswa.views import convert_date
from page_siswa.models import Siswa, list_events, list_notifikasi, sekolah
# Create your views here.


def homepage(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    siswa = Siswa.object.all()
    laki = siswa.filter(jenis_kelamin='Laki-Laki')
    perempuan = siswa.filter(jenis_kelamin='Perempuan')
    status = {
        'identitas': len(siswa.filter(status=0)),
        'upload_berkas': len(siswa.filter(status=1)),
        'verifikasi': len(siswa.filter(status=3)),
        'gagal_verifikasi': len(siswa.filter(status=4))
    }
    data = {'jumlah': len(siswa), 'laki': len(laki), 'perempuan': len(perempuan),
            'status': status}
    return render(request=request,
                  template_name='page_admin/beranda.html',
                  context={'data': data, 'active': 'beranda', 'setting': setting})


def listsiswa(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    siswa = Siswa.object.all()
    list_siswa = Siswa.object.order_by('nis')
    paginator = Paginator(list_siswa, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        alasan = request.POST.get('alasan')
        siswa = Siswa.object.get(nis=request.POST.get('nis_siswa'))
        list_notifikasi.objects.create(siswa=siswa, notifikasi=alasan)
        messages.success(request, f'Pesan berhasil dikirimkan')
    return render(request=request,
                  template_name='page_admin/tabelSiswa.html',
                  context={'list_siswa': page_obj, 'active': 'list', 'setting': setting})


def pageSeleksi(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    data_siswa = Siswa.object.all()
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    zonasi = {
        'jumlah': len(data_siswa.filter(status=10)),
        'kuota': json.loads(data_sekolah.pembagian_kuota())['zonasi']
    }
    afirmasi = {
        'jumlah': len(data_siswa.filter(status=11)),
        'kuota': json.loads(data_sekolah.pembagian_kuota())['afirmasi']
    }
    perpindahan = {
        'jumlah': len(data_siswa.filter(status=12)),
        'kuota': json.loads(data_sekolah.pembagian_kuota())['perpindahan']
    }
    prestasi = {
        'jumlah': len(data_siswa.filter(status=13)),
        'kuota': json.loads(data_sekolah.pembagian_kuota())['prestasi']
    }
    return render(request=request,
                  template_name='page_admin/seleksi_siswa.html',
                  context={'active': 'seleksi', 'data': [zonasi, afirmasi, perpindahan, prestasi]})


def tabelSeleksi2(request, data):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    first_time = False
    seleksi = {
        'nama': data.title()
    }
    alamat_sekolah = json.loads(data_sekolah.split_alamat())
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    if data == 'zonasii' or data == 'afirmasii' or data == 'perpiindahan' or data == 'prestasii':
        first_time = True
    if data == 'zonasi' or data == 'zonasii':
        list_siswa = Siswa.object.filter(status=10).annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
        seleksi['kuota'] = data_sekolah.sisa_zonasi
        seleksi['jumlah_siswa'] = len(list_siswa)
        seleksi['sisa_kuota'] = data_sekolah.sisa_zonasi - len(list_siswa)
        kab = []
        kec = []
        des = []
        for x in list_siswa:
            if x.get_desa_siswa() == alamat_sekolah['desa']:
                des.append(x)
            elif x.get_kecamatan_siswa() == alamat_sekolah['kecamatan']:
                kec.append(x)
            elif x.get_kabupaten_siswa() == alamat_sekolah['kabupaten']:
                kab.append(x)
        list_siswa = {}
        list_siswa['kabupaten'] = kab
        list_siswa['kecamatan'] = kec
        list_siswa['desa'] = des
    elif data == 'afirmasi' or data == 'afirmasii':
        list_siswa = Siswa.object.filter(status=11).annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
        seleksi['kuota'] = data_sekolah.sisa_afirmasi
        seleksi['jumlah_siswa'] = len(list_siswa)
        seleksi['sisa_kuota'] = data_sekolah.sisa_afirmasi - len(list_siswa)
    elif data == 'perpindahan' or data == 'perpiindahan':
        list_siswa = Siswa.object.filter(status=12).annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
        seleksi['kuota'] = data_sekolah.sisa_perpindahan
        seleksi['jumlah_siswa'] = len(list_siswa)
        seleksi['sisa_kuota'] = data_sekolah.sisa_perpindahan - len(list_siswa)
    elif data == 'prestasi' or data == 'prestasii':
        list_siswa = Siswa.object.filter(status=13).annotate(
            avg=(F('nilai_matematika') + F('nilai_ipa') + F('nilai_indonesia') + F('nilai_inggris'))/4).order_by('-avg')
        seleksi['kuota'] = data_sekolah.sisa_prestasi
        seleksi['jumlah_siswa'] = len(list_siswa)
        seleksi['sisa_kuota'] = data_sekolah.sisa_prestasi - len(list_siswa)
    else:
        messages.error(request, f'Terjadi Kesalahan')
        return redirect('admin_page:seleksi')
    if request.method == 'POST':
        data = request.POST.get('data')
        if data == 'Zonasi' or data == 'Zonasii':
            count = seleksi['kuota']
            for x in list_siswa['desa']:
                if(count >= 0):
                    # print('desa')
                    count -= 1
                    x.status = 5
                    x.save()
            for x in list_siswa['kecamatan']:
                if(count >= 0):
                    # print('kecamatan')
                    count -= 1
                    x.status = 5
                    x.save()
            for x in list_siswa['kabupaten']:
                if(count >= 0):
                    # print('kabupaten')
                    count -= 1
                    x.status = 5
                    x.save()
            if count > 0:
                data_sekolah.sisa_zonasi = 0
                data_sekolah.sisa_prestasi = data_sekolah.sisa_prestasi + count
                data_sekolah.save()
            messages.success(request,f'Seleksi Untuk Jalur Zonasi Berhasil Di selesaikan')
            return redirect('admin_page:seleksi')
        elif data == 'Afirmasi' or data == 'Afirmasii':
            count = seleksi['kuota']
            for x in list_siswa:
                if(count >= 0):
                    count -= 1
                    x.status = 5
                    x.save()
            if count > 0:
                data_sekolah.sisa_afirmasi = 0
                data_sekolah.sisa_prestasi = data_sekolah.sisa_prestasi + count
                data_sekolah.save()
            messages.success(request,f'Seleksi Untuk Jalur Afirmasi Berhasil Di selesaikan')
            return redirect('admin_page:seleksi')
        elif data == 'Perpindahan' or data == 'Perpiindahan':
            count = seleksi['kuota']
            for x in list_siswa:
                if(count >= 0):
                    count -= 1
                    x.status = 5
                    x.save()
            if count > 0:
                data_sekolah.sisa_perpindahan = 0
                data_sekolah.sisa_prestasi = data_sekolah.sisa_prestasi + count
                data_sekolah.save()
            messages.success(request,f'Seleksi Untuk Jalur Perpindahan Orang Tua Berhasil Di selesaikan')
            return redirect('admin_page:seleksi')
        elif data == 'Prestasi' or data == 'Prestasii':
            count = seleksi['kuota']
            for x in list_siswa:
                if(count >= 0):
                    count -= 1
                    x.status = 5
                    x.save()
            if count > 0:
                data_sekolah.sisa_perpindahan = 0
                data_sekolah.sisa_prestasi = data_sekolah.sisa_prestasi + count
                data_sekolah.save()
            messages.success(request,f'Seleksi Untuk Jalur Prestasi Berhasil Di selesaikan')
            return redirect('admin_page:seleksi')

    return render(request=request,
                  template_name='page_admin/tabelSeleksi2.html',
                  context={'list_siswa': list_siswa, 'active': 'seleksi', 'data_sekolah': data_sekolah, 'seleksi': seleksi, 'first_time': first_time})


def prosesSeleksi(request):
    data_sekolah = sekolah.objects.first()
    if request.method == 'POST':
        nis = request.POST.get('nis')
        data = request.POST.get('data').lower()
        hasil = request.POST.get('hasilSeleksi')
        alasan = "Pendaftaran di Tolak : " + request.POST.get('alasan')
        siswa = Siswa.object.get(nis=nis)
        if hasil == 'tolak':
            siswa.status = 7
        elif hasil == 'terima':
            siswa.status = 5
        siswa.save()
        if data == 'afirmasi':
            list_notifikasi.objects.create(siswa=siswa, notifikasi=alasan)
            messages.error(request, f'Seleksi untuk calon siswa {nis}, Berhasil ditolak')
            return redirect('admin_page:list_seleksi', 'afirmasi')
        elif data == 'zonasi' or data == 'zonasii':
            list_notifikasi.objects.create(siswa=siswa, notifikasi=alasan)
            messages.error(request, f'Seleksi untuk calon siswa {nis}, Berhasil ditolak')
            return redirect('admin_page:list_seleksi', 'zonasi')
        elif data == 'perpindahan':
            messages.success(request, f'Seleksi Berhasil')
            return redirect('admin_page:list_seleksi', data)
        elif data == 'prestasi':
            messages.success(request, f'Seleksi Berhasil')
            return redirect('admin_page:list_seleksi', data)


def tabelSeleksi(request, data):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    error = ''
    data_sekolah = sekolah.objects.first()
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    siswa = Siswa.object.all()
    if request.method == 'GET':
        error = request.GET.get('error')
    s = 10
    ass = Siswa.object.annotate(
        avg=(F('nilai_matematika')+F('nilai_indonesia')+F('nilai_ipa')+F('nilai_inggris')/4))[:s]
    list_siswa = Siswa.object.filter(status=6)
    paginator = Paginator(list_siswa, 7)
    page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        if request.POST.get('jumlahSiswa'):
            jumlah = request.POST.get('jumlahSiswa')
            if int(request.POST.get('jumlahSiswa')) > list_siswa.count():
                response = redirect('admin_page:seleksi')
                response['Location'] += '?error=otomatis'
                messages.error(
                    request, f'Jumlah Siswa Yang Ingin Diterima Melebihi dari siswa yang sudah terverifikasi')
                return response
            else:
                siswa_seleksi = Siswa.object.annotate(
                    avg=(F('nilai_matematika')+F('nilai_indonesia')+F('nilai_ipa')+F('nilai_inggris')/4))[:jumlah]
        else:
            for x in request.POST:
                if request.POST[x] == 'Ya':
                    siswa = list_siswa.get(nis=x)
                    siswa.status = 5
                    siswa.save()
                elif request.POST[x] == 'Tidak':
                    siswa = list_siswa.get(nis=x)
                    siswa.status = 7
                    siswa.save()
            return redirect('admin_page:home')
    return render(request=request,
                  template_name='page_admin/tabelSeleksi.html',
                  context={'list_siswa': list_siswa, 'active': 'seleksi', 'error': error, 'setting': setting})


def verifikasi_siswa(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    list_siswa = Siswa.object.filter(status=3).order_by('nis')
    data_sekolah = sekolah.objects.first()
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    siswa = Siswa.object.all()
    paginator = Paginator(list_siswa, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        siswa = Siswa.object.get(nis=request.POST.get('nis_siswa'))
        if request.POST.get('check') == 'terima':
            alasan = 'Verifikasi Berhasil'
            siswa.status = 6
            siswa.save()
            list_notifikasi.objects.create(siswa=siswa, notifikasi=alasan)
            messages.success(
                request, f'Status siswa {siswa.nis} berhasil diverifikasi')
            return redirect('admin_page:verifikasi_siswa')
        elif request.POST.get('check') == 'tolak':
            alasan = 'Verifikasi Gagal : {}'.format(request.POST.get('alasan'))
            siswa.status = 4
            siswa.save()
            list_notifikasi.objects.create(siswa=siswa, notifikasi=alasan)
            messages.success(
                request, f'Status siswa {siswa.nis} gagal diverifikasi dengan alasan {alasan}')
            return redirect('admin_page:verifikasi_siswa')
        elif request.POST.get('check') == 'pesan':
            alasan = request.POST.get('alasan')
            list_notifikasi.objects.create(siswa=siswa, notifikasi=alasan)
            messages.success(request, f'Pesan berhasil dikirimkan')
            return redirect('admin_page:verifikasi_siswa')
    return render(request=request,
                  template_name='page_admin/tabelVerifikasiSiswa.html',
                  context={'list_siswa': page_obj, 'active': 'verifikasi', 'setting': setting})


def events(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    data_sekolah = sekolah.objects.first()
    setting = False
    if data_sekolah.nama == '' or data_sekolah.alamat == '' or data_sekolah.daya_tampung == 0:
        setting = True
    siswa = Siswa.object.all()
    event = list_events.objects.all()
    if request.method == 'POST':
        if request.POST.get('event'):
            nama = request.POST.get('event')
            awal = convert_date(request.POST.get('mulai'))
            akhir = convert_date(request.POST.get('akhir'))
            list_events.objects.create(
                name=nama, start_date=awal, end_date=akhir)
            messages.success(request, f'Event Berhasil Ditambahkan')
            return redirect('admin_page:events')
        elif request.POST.get('id'):
            id = request.POST.get('id')
            event = list_events.objects.get(id=id)
            event.delete()
            messages.success(request, f'Event Berhasil Dihapus')
            return redirect('admin_page:events')
    return render(request=request,
                  template_name='page_admin/events.html',
                  context={'active': 'events', 'events': event, 'setting': setting})


def setting_ppdb(request):
    data_sekolah = sekolah.objects.first()
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    if request.method == 'POST':
        if request.POST.get('dayaTampung'):
            sisa = json.loads(data_sekolah.pembagian_kuota())
            # siswa_update = Siswa.object.filter(Q(status=10) | Q(status=11) | Q(status=12) | Q(status=13))
            kuota = request.POST.get('dayaTampung')
            zonasi = request.POST.get('zonasi')
            afirmasi = request.POST.get('afirmasi')
            perpindahan = request.POST.get('perpindahan')
            prestasi = request.POST.get('prestasi')
            data_sekolah.daya_tampung = kuota
            data_sekolah.sisa_zonasi = int(
                zonasi) + (sisa['zonasi'] - data_sekolah.sisa_zonasi)
            data_sekolah.sisa_afirmasi = int(
                afirmasi) + (sisa['afirmasi'] - data_sekolah.sisa_afirmasi)
            data_sekolah.sisa_perpindahan = int(
                perpindahan) + (sisa['perpindahan'] - data_sekolah.sisa_perpindahan)
            data_sekolah.sisa_prestasi = int(
                prestasi) + (sisa['prestasi'] - data_sekolah.sisa_prestasi)
            data_sekolah.save()
            messages.success(request, f'Daya Tampung Sekolah Berhasil di Ubah')
            return redirect('admin_page:setting')
        elif request.POST.get('status'):
            status = request.POST.get('status')
            data_sekolah.status_pendaftaran = status
            data_sekolah.save()
            messages.success(request, f'Status PPDB Berhasil diubah')
            return redirect('admin_page:setting')
        elif request.POST.get('nama_sekolah'):
            nama = request.POST.get('nama_sekolah')
            data_sekolah.nama = nama
            data_sekolah.save()
            messages.success(request, f'Nama Sekolah Berhasil Diubah')
            return redirect('admin_page:setting')
        elif request.POST.get('desa'):
            prov = request.POST['prov']
            kab = request.POST['kab']
            kec = request.POST['kec']
            desa = request.POST['desa']
            alamat = f'provinsi: {prov}, kabupaten: {kab}, kecamatan: {kec}, desa: {desa}'
            data_sekolah.alamat = alamat
            data_sekolah.save()
            messages.success(request, f'Alamat Sekolah Berhasil Diubah')
            return redirect('admin_page:setting')
    return render(request=request,
                  template_name='page_admin/settings.html',
                  context={'active': 'setting', 'data_sekolah': data_sekolah})
