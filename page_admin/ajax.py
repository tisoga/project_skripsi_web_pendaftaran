from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from page_siswa.models import Siswa, CustomUser

from api.serializer import ListSiswaSerializer


@api_view(['GET','POST'])
def list_siswa(request):
    sort = int(request.GET.get('sort'))
    if sort == 0:
        list_siswa = Siswa.object.all()
    elif sort == 10:
        list_siswa = Siswa.object.filter(jalur_pendaftaran = 'Zonasi')
    elif sort == 11:
        list_siswa = Siswa.object.filter(jalur_pendaftaran = 'Afirmasi')
    elif sort == 12:
        list_siswa = Siswa.object.filter(jalur_pendaftaran = 'Perpindahan OrangTua')
    elif sort == 13:
        list_siswa = Siswa.object.filter(jalur_pendaftaran = 'Prestasi')
    else:
        list_siswa = Siswa.object.filter(status=sort)
    # elif sort == '1':
    #     list_siswa = Siswa.object.filter(status=0)
    # elif sort == '2':
    #     list_siswa = Siswa.object.filter(status=1)
    # elif sort == '3':
    #     list_siswa = Siswa.object.filter(status=3)
    if request.method == 'GET':
        # print(list_siswa)
        serializer = ListSiswaSerializer(list_siswa, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def pembagian_kuota(request):
    if request.method == 'GET':
        try:
            jumlah_siswa = int(request.GET.get('daya_tampung'))
            zonasi = int(jumlah_siswa * 0.50)
            afirmasi = int(jumlah_siswa * 0.15)
            perpindahan = int(jumlah_siswa * 0.05)
            prestasi = int(jumlah_siswa * 0.30)
            sisa = jumlah_siswa - (zonasi + afirmasi + perpindahan + prestasi)

            data = {'zonasi': zonasi, 'afirmasi': afirmasi, 'perpindahan': perpindahan, 'prestasi': prestasi+sisa}
            return Response(data)
        except:
            return Response({"message": "Terjadi Kesalahan"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Terjadi Kesalahan"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getSiswaSeleksi(request):
    if request.method == 'GET':
        daftar_siswa = Siswa.object.all()
        serializer = ListSiswaSerializer(daftar_siswa, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def check_password(request):
    if request.method == 'POST':
        id_user = request.data.get('id')
        old = request.data.get('old_password')
        if not old:
            return Response({"error": "Password Lama Tidak Boleh Kosong"}, status=status.HTTP_400_BAD_REQUEST)
        elif not id_user:
            return Response({"error": "Terjadi Kesalahan Silahkan Reload Ulang Page ini."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, id=id_user)
        if user.check_password(old):
            return Response({"proses": "verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Harap Masukan Password Lama Yang Benar"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def new_password(request):
    if request.method == "POST":
        id_user = request.data.get('id')
        new = request.data.get('new_password')
        confirm = request.data.get('confirm_password')
        if not (new and confirm):
            return Response({"error": "Password baru dan Password Confirm Tidak Boleh Kosong"}, status=status.HTTP_400_BAD_REQUEST)
        elif not id_user:
            return Response({"error": "Terjadi Kesalahan Silahkan Reload Ulang Page ini."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, id=id_user)
        if new == confirm:
            user.set_password(new)
            user.save()
            # update_session_auth_hash(request, user)
            return Response({"proses": "Password Berhasil di ubah."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Password Tidak Sesuai"}, status=status.HTTP_400_BAD_REQUEST)