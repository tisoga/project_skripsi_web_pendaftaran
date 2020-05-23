from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializer import ListSiswaSerializer

from page_siswa.models import Siswa
# Create your views here.

@api_view(['GET'])
def ProfileAPI(request, nis):
    siswa = get_object_or_404(Siswa, nis = nis)
    if request.method == 'GET':
        serializer = ListSiswaSerializer(siswa)
        return Response(serializer.data, status=status.HTTP_200_OK)