function open_modal(val) {
    var html_pendaftaran = `
        <h5>Harap Periksa Kembali Data-data Anda Sebelum Mengirimkan Pengajuan.</h5>
        <h5>Dikarenakan <b>Jika Anda Sudah Mengirimkan Pengajuan, Anda TIdak Dapat Merubah Kembali Data Anda.</b></h5>
    `
    if (val == 'first'){
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
    else if (val == 'Send')
    {
        document.getElementById('ModalLongTitle').innerHTML = 'Peringatan';
        document.getElementById('modal-body').innerHTML = html_pendaftaran;
        document.getElementById('btn_no').innerHTML = 'Tidak';
        document.getElementById('btn_no').className = 'btn btn-secondary';
        document.getElementById('btn_yes').style.display = 'block'
        document.getElementById('btn_yes').innerHTML = 'Ajukan Pendaftaran';
        $('#ModalCenter').modal({ backdrop: 'static', keyboard: true });
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