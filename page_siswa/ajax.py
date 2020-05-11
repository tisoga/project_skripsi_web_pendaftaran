import requests
from django.http import JsonResponse

def get_provinsi(request):
    url = 'https://dev.farizdotid.com/api/daerahindonesia/provinsi'
    res = requests.get(url)
    data = res.json()
    return JsonResponse(data)

def get_kota(request, id):
    url = 'https://dev.farizdotid.com/api/daerahindonesia/kota?id_provinsi={}'.format(id)
    res = requests.get(url)
    data = res.json()
    return JsonResponse(data)

def get_kecamatan(request, id):
    url = 'https://dev.farizdotid.com/api/daerahindonesia/kecamatan?id_kota={}'.format(id)
    res = requests.get(url)
    data = res.json()
    return JsonResponse(data)

def get_kelurahan(request, id):
    url = 'https://dev.farizdotid.com/api/daerahindonesia/kelurahan?id_kecamatan={}'.format(id)
    res = requests.get(url)
    data = res.json()
    return JsonResponse(data)
    