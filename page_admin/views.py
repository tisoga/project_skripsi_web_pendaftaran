from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse

from page_siswa.models import Siswa
# Create your views here.


def homepage(request):
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
                  template_name = 'page_admin/beranda.html',
                  context = {'data': data})

def listsiswa(request):
    list_siswa = Siswa.object.all()
    paginator = Paginator(list_siswa, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    # test = list(page_obj.object_list.values())
    # json = JsonResponse(test, safe=False)
    # print(json.content)
    return render(request=request,
                  template_name = 'page_admin/tabelSiswa.html',
                  context = {'list_siswa': page_obj})