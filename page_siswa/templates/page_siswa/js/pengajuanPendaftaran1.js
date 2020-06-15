function pilihJalur(val) {
    var textZonasi = `Jalur Zonasi adalah Jalur Pendaftaran untuk para calon siswa yang berdomisili dalam satu wilayah kabupaten/kota dengan sekolah berasal.`
    var textAfirmasi = `Jalur Afirmasi adalah Jalur Pendaftaran untuk para calon siswa yang menerima program penanganan keluarga tidak mampu dari pemerintah pusat ataupun pemerintah daerah, harus menyertakan bukti mengikuti penanganan keluarga tidak mampu.`
    var textPerpindahan = `Jalur Perpindahan Orangtua / Wali adalah Jalur Pendaftaran untuk para calon siswa yang baru pindah domisili dikarenakan mengikuti tugas atau pekerjaan orang tua / wali, harus menyertakan surat penugasan dari instansi atau perusahaan yang mengerjakan orang tua / wali.`
    var textPrestasi = `Jalur Prestasi adalah Jalur Pendaftaran untuk para calon siswa yang mimiliki prestasi yang ditentukan berdasarkan hasil nilai ujian sekolah atau UN (ujian nasional), hasil perlombaan  atau penghargaan di bidang akademik atau non-akademik.`
    var kabupatenSiswa = '{{request.user.DetailUser.get_kabupaten_siswa}}'
    var alamatSekolah = JSON.parse('{{sekolah.split_alamat|safe}}')
    $('#cardPenjelasan').show();
    $('#fileUpload').show();
    switch (val) {
        case 'zonasi':
            $('#hiddenID').val('zonasi');
            $('#textPengertian').text(textZonasi);
            $('#btnZonasi').removeClass('btn-primary').addClass('btn-success');
            $('#btnAfirmasi').removeClass('btn-success').addClass('btn-primary');
            $('#btnPerpindahan').removeClass('btn-success').addClass('btn-primary');
            $('#btnPrestasi').removeClass('btn-success').addClass('btn-primary');
            $('#fileUpload').hide();
            if (kabupatenSiswa != alamatSekolah.kabupaten) {
                $('#btn_yes2').attr('disabled', true);
                $('#zonasiPeringatan').show()
            }
            break;
        case 'afirmasi':
            $('#inputUpload').val('');
            $('#hiddenID').val('afirmasi');
            $('#textPengertian').text(textAfirmasi);
            $('#btnZonasi').removeClass('btn-success').addClass('btn-primary');
            $('#btnAfirmasi').removeClass('btn-primary').addClass('btn-success');
            $('#btnPerpindahan').removeClass('btn-success').addClass('btn-primary');
            $('#btnPrestasi').removeClass('btn-success').addClass('btn-primary');
            $('#labelUpload').text('Upload Bukti Mengikuti Penanganan Keluarga Tidak Mampu')
            $('#inputUpload').attr('name', 'afirmasi');
            $('#inputUpload').attr('required', true);
            $('#btn_yes2').attr('disabled', false);
            $('#zonasiPeringatan').hide();
            break;
        case 'perpindahan':
            $('#inputUpload').val('');
            $('#hiddenID').val('perpindahan');
            $('#textPengertian').text(textPerpindahan);
            $('#btnZonasi').removeClass('btn-success').addClass('btn-primary');
            $('#btnAfirmasi').removeClass('btn-success').addClass('btn-primary');
            $('#btnPerpindahan').removeClass('btn-primary').addClass('btn-success');
            $('#btnPrestasi').removeClass('btn-success').addClass('btn-primary');
            $('#labelUpload').text('Upload Surat Penugasan dari Instansi atau Perusahaan')
            $('#inputUpload').attr('name', 'perpindahan');
            $('#inputUpload').attr('required', true);
            $('#btn_yes2').attr('disabled', false);
            $('#zonasiPeringatan').hide();
            break;
        case 'prestasi':
            $('#inputUpload').val('');
            $('#hiddenID').val('prestasi');
            $('#textPengertian').text(textPrestasi);
            $('#btnZonasi').removeClass('btn-success').addClass('btn-primary');
            $('#btnAfirmasi').removeClass('btn-success').addClass('btn-primary');
            $('#btnPerpindahan').removeClass('btn-success').addClass('btn-primary');
            $('#btnPrestasi').removeClass('btn-primary').addClass('btn-success');
            $('#labelUpload').text('Upload Sertifikat Penghargaan *Optional')
            $('#inputUpload').attr('name', 'prestasi');
            $('#inputUpload').attr('required', false);
            $('#btn_yes2').attr('disabled', false);
            $('#zonasiPeringatan').hide();
            break;
    }
}

function open_modal(val) {
    var html_pendaftaran = `
        <h5>Harap Periksa Kembali Data-data Anda Sebelum Mengirimkan Pengajuan.</h5>
        <h5>Dikarenakan <b>Jika Anda Sudah Mengirimkan Pengajuan, Anda TIdak Dapat Merubah Kembali Data Anda.</b></h5>
    `
    if (val == 'first') {
        document.getElementById('ModalLongTitle').innerHTML = 'Peringatan';
        document.getElementById('modal-body').innerHTML = html_pendaftaran;
        document.getElementById('btn_no').innerHTML = 'Ya';
        document.getElementById('btn_no').className = 'btn btn-primary';
        document.getElementById('btn_yes').style.display = 'none'
        $('#ModalCenter').modal({ backdrop: 'static', keyboard: true });
    }
    else if (val == 'Simpan') {
        document.getElementById('ModalLongTitle').innerHTML = 'Peringatan';
        document.getElementById('modal-body').innerHTML = 'Apakah anda yakin ingin mengedit data siswa ?';
        document.getElementById('btn_no').innerHTML = 'Tidak';
        document.getElementById('btn_no').className = 'btn btn-secondary';
        document.getElementById('btn_yes').style.display = 'block'
        document.getElementById('btn_yes').innerHTML = 'Ya';
        $('#ModalCenter').modal({ backdrop: 'static', keyboard: true });
    }
    else if (val == 'Send') {
        $('#modalPilihJalur').modal('hide')
        document.getElementById('ModalLongTitle2').innerHTML = 'Peringatan';
        document.getElementById('modal-body2').innerHTML = html_pendaftaran;
        document.getElementById('btn2_no').innerHTML = 'Tidak';
        document.getElementById('btn2_no').className = 'btn btn-secondary';
        document.getElementById('btn2_yes').style.display = 'block'
        document.getElementById('btn2_yes').innerHTML = 'Ajukan Pendaftaran';
        $('#modalPengajuan').modal({ backdrop: 'static', keyboard: true });
    }
}
function split_alamat() {
    var val = '{{request.user.DetailUser.alamat}}';
    var alamats = document.getElementsByClassName('alamat_lengkap');
    var sel = document.getElementsByClassName('alamat_select');
    var id = document.getElementById('edit_alamat');
    if (id.checked == true) {
        var data = val.split(",");
        for (var i = 0; i < sel.length; i++) {
            // var option = document.createElement("option");
            // option.text = data[4 - i];
            // option.disabled = true;
            // option.hidden = true;
            // option.selected = true
            // sel[i].add(option);
            sel[i].required = true;
        }
        alamats[0].disabled = false;
        alamats[0].required = true;
        alamats[0].value = data[0];
        for (var i = 1; i < alamats.length; i++) {
            alamats[i].style.display = 'block';
        }
    }
    else {
        for (var i = 0; i < sel.length; i++) {
            sel[i].required = false;
        }
        alamats[0].disabled = true;
        alamats[0].required = false;
        alamats[0].value = val;
        for (var i = 1; i < alamats.length; i++) {
            alamats[i].style.display = 'none';
        }
    }
}
function upload_ulang(file) {
    btn = document.getElementById(file);
    if (btn.checked == true) {
        switch (file) {
            case 'edit_ijazah':
                document.getElementById('ijazah').style.display = 'block';
                document.getElementById('input_ijazah').required = true;
                break;
            case 'edit_akta':
                document.getElementById('akta').style.display = 'block';
                document.getElementById('input_akta').required = true;
                break;
            case 'edit_kesehatan':
                document.getElementById('kesehatan').style.display = 'block';
                document.getElementById('input_kesehatan').required = true;
                break;
            case 'edit_foto':
                document.getElementById('foto').style.display = 'block';
                document.getElementById('input_foto').required = true;
                break;
        }
    }
    else if (btn.checked == false) {
        switch (file) {
            case 'edit_ijazah':
                document.getElementById('ijazah').style.display = 'none';
                document.getElementById('input_ijazah').value = '';
                document.getElementById('input_ijazah').required = false;
                break;
            case 'edit_akta':
                document.getElementById('akta').style.display = 'none';
                document.getElementById('input_akta').value = '';
                document.getElementById('input_akta').required = false;
                break;
            case 'edit_kesehatan':
                document.getElementById('kesehatan').style.display = 'none';
                document.getElementById('input_kesehatan').value = '';
                document.getElementById('input_kesehatan').required = false;
                break;
            case 'edit_foto':
                document.getElementById('foto').style.display = 'none';
                document.getElementById('input_foto').value = '';
                document.getElementById('input_foto').required = false;
                break;
        }
    }
};
function editData(check) {
    var btn = document.getElementById('btn_edit');
    var inputs = document.getElementsByClassName('editabled');
    var alamats = document.getElementsByClassName('alamat_lengkap');
    var radio = document.getElementsByClassName('form-check-input');
    var hidden = document.getElementsByClassName('hidden');
    if (check == 'edit') {
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].disabled = false;
        }
        document.getElementById('decision').value = 'edit';
        document.getElementById('btn_cancel').style.display = 'block';
        document.getElementById('btn_pendaftaran').style.display = 'none';
        hidden[0].style.display = 'block';
        btn.value = 'save';
        btn.innerHTML = 'Simpan';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-primary');
        for (var i = 0; i < radio.length; i++) {
            if (radio[i].checked == false) {
                radio[i].disabled = false;
            }
        }
        for (var i = 1; i < 4; i++) {
            hidden[i].style.display = 'none';
        }
        for (var i = 4; i < hidden.length; i++) {
            hidden[i].style.display = 'block';
        }
    }
    else if (check == 'save') {
        open_modal('Simpan');
    }
    else if (check == 'Cancel') {
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].disabled = true;
        }
        for (var i = 1; i < alamats.length; i++) {
            alamats[i].style.display = 'none';
        }
        hidden[0].style.display = 'none';
        document.getElementById('edit_alamat').checked = false;
        alamats[0].innerHTML = '{{request.user.DetailUser.alamat}}'
        btn.value = 'edit'
        btn.innerHTML = 'Edit'
        btn.classList.remove('btn-primary')
        btn.classList.add('btn-success')
        for (var i = 0; i < radio.length; i++) {
            if (radio[i].checked == false) {
                radio[i].disabled = true;
            }
        }
        for (var i = 1; i < 4; i++) {
            hidden[i].style.display = 'block';
        }
        for (var i = 4; i < hidden.length; i++) {
            hidden[i].style.display = 'none';
        }
    }

}