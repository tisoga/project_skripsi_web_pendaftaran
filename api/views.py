import json
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .serializer import ListSiswaSerializer, LoginSerializer, \
    UserSerializer, RegisterSerializer, PelengkapanIdentitasSerializer, \
    PelengkapanBerkasSerializer, KegiatanSerializer, NotifikasiSerializer, PengajuanPendaftaranSerializer, EditPengajuanSerializer, SekolahSerializer

from knox.auth import AuthToken

from page_siswa.models import Siswa, list_events, list_notifikasi, sekolah
# Create your views here.


@api_view(['GET'])
def ProfileAPI(request, nis):
    siswa = get_object_or_404(Siswa, nis=nis)
    if request.method == 'GET':
        serializer = ListSiswaSerializer(siswa)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def LoginAPI(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                'user': UserSerializer(user, context=serializer).data,
                'token': AuthToken.objects.create(user)[1]
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def RegisterAPI(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                ListSiswaSerializer(user, context=serializer).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def ProfileSiswaAPI(request):
    siswa = get_object_or_404(Siswa, nis=request.user.DetailUser.nis)
    if request.method == 'GET':
        serializer = ListSiswaSerializer(siswa)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = PelengkapanIdentitasSerializer(siswa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = ListSiswaSerializer(siswa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UploadBerkasAPI(request):
    siswa = get_object_or_404(Siswa, nis=request.user.DetailUser.nis)
    if request.method == 'PUT':
        serializer = PelengkapanBerkasSerializer(siswa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def PengajuanAPI(request):
    siswa = get_object_or_404(Siswa, nis=request.user.DetailUser.nis)
    if request.method == 'PUT':
        serializer = PengajuanPendaftaranSerializer(siswa, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = EditPengajuanSerializer(siswa, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListKegiatanAPI(request):
    events = list_events.objects.all()
    if request.method == 'GET':
        serializer = KegiatanSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def NotifikasiAPI(request):
    notif = get_list_or_404(list_notifikasi, siswa=request.user.id)
    if request.method == 'GET':
        serializer = NotifikasiSerializer(notif, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def SekolahAPI(request):
    data_sekolah = sekolah.objects.first()
    split_alamat = json.loads(data_sekolah.split_alamat()) 
    data_sekolah.alamat_lengkap_split = {
        'lengkap': data_sekolah.alamat_lengkap,
        'desa': split_alamat['desa'],
        'kecamatan': split_alamat['kecamatan'],
        'kabupaten': split_alamat['kabupaten'],
        'provinsi': split_alamat['provinsi'],

    }
    data_sekolah.jam_tanggal_ulang = data_sekolah.split_tanggal_jam()
    if request.method == 'GET':
        serializer = SekolahSerializer(data_sekolah)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)