from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.paginator import Paginator
from django.http import JsonResponse
from page_siswa.models import Siswa

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
        list_siswa = Siswa.object.filter(jalur_pendaftaran = 'Perpindahan')
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