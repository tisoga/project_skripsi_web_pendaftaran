from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.paginator import Paginator

from page_siswa.models import Siswa

from api.serializer import ListSiswaSerializer


@api_view(['GET','POST'])
def list_siswa(request):
    sort = request.GET.get('sort')
    if sort == '0':
        list_siswa = Siswa.object.all()
    elif sort == '1':
        list_siswa = Siswa.object.filter(status=0)
    elif sort == '2':
        list_siswa = Siswa.object.filter(status=1)
    elif sort == '3':
        list_siswa = Siswa.object.filter(status=3)
    if request.method == 'GET':
        serializer = ListSiswaSerializer(list_siswa, many=True)
        return Response(serializer.data)
