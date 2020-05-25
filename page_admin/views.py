from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from page_siswa.views import convert_date
from page_siswa.models import Siswa, list_events, list_notifikasi
# Create your views here.


def homepage(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
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
                  context={'data': data, 'active': 'beranda'})


def listsiswa(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    list_siswa = Siswa.object.all()
    paginator = Paginator(list_siswa, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        alasan = request.POSt.get('alasan')
        siswa = Siswa.object.get(nis = request.POST.get('nis_siswa'))
        list_notifikasi.objects.create(siswa = siswa, notifikasi = alasan)
        messages.success(request, f'Pesan berhasil dikirimkan')
    return render(request=request,
                  template_name='page_admin/tabelSiswa.html',
                  context={'list_siswa': page_obj, 'active': 'list'})


def verifikasi_siswa(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    list_siswa = Siswa.object.filter(status=3).order_by('nis')
    paginator = Paginator(list_siswa, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        siswa = Siswa.object.get(nis = request.POST.get('nis_siswa'))
        if request.POST.get('check') == 'terima':
            alasan = 'Verifikasi Berhasil'
            siswa.status = 6
            siswa.save()
            list_notifikasi.objects.create(siswa = siswa, notifikasi = alasan)
            messages.success(request, f'Status siswa {siswa.nis} berhasil diverifikasi')
            return redirect('admin_page:verifikasi_siswa')
        elif request.POST.get('check') == 'tolak':
            alasan = 'Verifikasi Gagal : {}'.format(request.POST.get('alasan'))
            siswa.status = 4
            siswa.save()
            list_notifikasi.objects.create(siswa = siswa, notifikasi = alasan)
            messages.success(request, f'Status siswa {siswa.nis} gagal diverifikasi dengan alasan {alasan}')
            return redirect('admin_page:verifikasi_siswa')
        elif request.POST.get('check') == 'pesan':
            alasan = request.POST.get('alasan')
            list_notifikasi.objects.create(siswa = siswa, notifikasi = alasan)
            messages.success(request, f'Pesan berhasil dikirimkan')
            return redirect('admin_page:verifikasi_siswa')
    return render(request=request,
                  template_name='page_admin/tabelVerifikasiSiswa.html',
                  context={'list_siswa': page_obj, 'active': 'verifikasi'})


def events(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('siswa:home')
    event = list_events.objects.all()
    if request.method == 'POST':
        if request.POST.get('event'):
            nama = request.POST.get('event')
            awal = convert_date(request.POST.get('mulai'))
            akhir = convert_date(request.POST.get('akhir'))
            list_events.objects.create(name=nama, start_date=awal, end_date=akhir)
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
                  context={'active': 'events', 'events': event})