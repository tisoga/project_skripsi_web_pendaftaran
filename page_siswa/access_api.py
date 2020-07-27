import json
import requests

base_url = '127.0.0.1/api'


def get_access_api(request, url, token=None):
    url = base_url + url
    response = request.post(url, headers={
        "authorization": token
    })
    if response.status_code == '401':
        return 'Token Invalid'
    elif response.status_code == '200':
        return response.json()
    else:
        return 'Terjadi Kesalahan'


def post_access_api(request, url, token=None):
    the_data = json.loads(request.POST)
    url = base_url + url
    response = request.post(url, data=the_data, headers={
        "authorization": token
    })
    if response.status_code == '401':
        return 'Token Invalid'
    elif response.status_code == '200':
        return response.json()
    else:
        return 'Terjadi Kesalahan'

def put_access_api(request, url, token=None):
    the_data = json.loads(request.POST)
    url = base_url + url
    response = request.put(url, data=the_data, headers={
        "authorization": token
    })
    if response.status_code == '401':
        return 'Token Invalid'
    elif response.status_code == '200':
        return response.json()
    else:
        return 'Terjadi Kesalahan'

def patch_access_api(request, url, token=None):
    the_data = json.loads(request.POST)
    url = base_url + url
    response = request.patch(url, data=the_data, headers={
        "authorization": token
    })
    if response.status_code == '401':
        return 'Token Invalid'
    elif response.status_code == '200':
        return response.json()
    else:
        return 'Terjadi Kesalahan'