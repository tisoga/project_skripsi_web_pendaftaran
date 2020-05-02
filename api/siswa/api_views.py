from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from knox.auth import AuthToken

from api.siswa.serializers import UserSerializer, LoginSerializer, RegisterSerializer, DetailUserSerializer

from django.shortcuts import get_object_or_404
from page_siswa.models import Siswa
@api_view(['POST'])
def loginAPI(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                'User': UserSerializer(user, context=serializer).data,
                'Token': AuthToken.objects.create(user)[1]
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
def RegisterAPI(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response('GET METHOD')


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def UserAPI(request):
    user = get_object_or_404(Siswa, pk = request.user)
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DetailUserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)