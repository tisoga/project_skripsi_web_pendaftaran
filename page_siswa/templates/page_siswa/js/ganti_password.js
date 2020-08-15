const text_peringatan = document.getElementById('modal-body');
const label_old = document.getElementById('label_old');
const label_new = document.getElementById('label_new');
const label_confirm = document.getElementById('label_confirm');
const input_old = document.getElementById('old_password');
const input_new = document.getElementById('new_password');
const input_confirm = document.getElementById('confirm_password');
const btn_check = document.getElementById('btn_check');
const btn_change = document.getElementById('btn_change');
const btn_modal = document.getElementById('btn_modal');

function check_password(id, password) {
    // console.log(id)
    if (!password) {
        text_peringatan.innerHTML = "Password Lama Tidak Boleh Kosong!";
        $('#modalPeringatan').modal('show');
    }
    else if (id === 'None' || !id) {
        text_peringatan.innerHTML = "Terjadi Kesalahan, Silahkan Coba Kembali.";
        $('#modalPeringatan').modal('show');
        btn_modal.setAttribute("onClick", "location.reload()");
    }
    else {
        const data = JSON.stringify({
            "id": id,
            "old_password": password
        })
        $.ajax({
            url: '{% url "admin_page:ajax_check_password" %}',
            type: 'POST',
            contentType: 'application/json',
            data: data,
            dataType: 'json',
            success: function (res) {
                // console.log(res)
                label_new.classList.remove('text-muted');
                label_confirm.classList.remove('text-muted');
                label_old.classList.add('text-muted');
                input_old.disabled = true;
                input_new.disabled = false;
                input_confirm.disabled = false;
                btn_check.disabled = true;
                btn_check.className = "btn btn-secondary mt-2";
                btn_change.disabled = false;
                btn_change.className = "btn btn-primary float-right mt-1";
            },
            error: function (request, status, error) {
                // console.log(request.responseJSON)
                text_peringatan.innerHTML = request.responseJSON.error;
                $('#modalPeringatan').modal('show');
                input_old.value = "";
            }
        })
    }
}

function ganti_password(id, new_password, confirm_password) {
    if (!new_password || !confirm_password) {
        text_peringatan.innerHTML = "Password Baru dan Konfirmasi Password tidak boleh kosong.";
        $('#modalPeringatan').modal('show');
    }
    else if (!id) {
        text_peringatan.innerHTML = "Terjadi Kesalahan, Silahkan Coba Kembali.";
        btn_modal.setAttribute("onClick", "location.reload()");
    }
    else {
        const data = JSON.stringify({
            "id": id,
            "new_password": new_password,
            "confirm_password": confirm_password
        })
        console.log(data)
        $.ajax({
            url: '{% url "admin_page:ajax_new_password" %}',
            type: 'POST',
            contentType: 'application/json',
            data: data,
            dataType: 'json',
            success: function (res) {
                // console.log(res)
                text_peringatan.innerHTML = "Password Berhasil Diubah, Silahkan Login Kembali!"
                btn_modal.setAttribute("onClick", "window.location.href = '{%url 'siswa:login'%}'");
                $('#modalPeringatan').modal({backdrop: 'static', keyboard: false});
            },
            error: function (request, status, error) {
                // console.log(request.responseJSON)
                text_peringatan.innerHTML = request.responseJSON.error;
                $('#modalPeringatan').modal('show');
            }
        })
    }
}

function close_modal() {
    $('#modalPeringatan').modal('hide');
}