$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: "{% url 'siswa:ajax_provinsi'%}",
        dataType: 'json',
        success: function (data) {
            // alert(data)
            $("#provinsi").attr('disabled', false);
            $.each(data.provinsi, function (key, value) {
                $("#provinsi").append('<option value=' + value.id + '>' + value.nama + '</option>');
            });
        },
        error: function(textStatus, errorThrown) { 
            alert("Status: " + textStatus.status); alert("Error: " + errorThrown); 
        } 
    });
});

$("#provinsi").change(function () {
    var id = $(this).val();
    $('#kabupaten')
        .find('option')
        .remove()
        .end()
        .append('<option value disabled selected>Silahkan Pilih</option>');
    $('#kecamatan')
        .find('option')
        .remove()
        .end()
        .append('<option value disabled selected>Silahkan Pilih</option>');
    $('#desa')
        .find('option')
        .remove()
        .end()
        .append('<option value disabled selected>Silahkan Pilih</option>');
    document.getElementById('prov').value = $("#provinsi option:selected").html();
    document.getElementById('kab').value = '';
    document.getElementById('kec').value = '';
    $.ajax({                       // initialize an AJAX request
        url: "{% url 'siswa:ajax_kota' 1234%}".replace(/1234/, id),
        dataType: 'json',
        success: function (data) {   // `data` is the return of the `load_cities` view function
            // alert(data.kabupatens)
            $("#kabupaten").attr('disabled', false);
            $.each(data.kota_kabupaten, function (key, value) {
                $("#kabupaten").append('<option value=' + value.id + '>' + value.nama + '</option>');
            });
        }
    });

});

    $("#kabupaten").change(function () {
        var id = $(this).val();  // get the selected country ID from the HTML input
        $('#kecamatan')
            .find('option')
            .remove()
            .end()
            .append('<option value disabled selected>Silahkan Pilih</option>');
        $('#desa')
            .find('option')
            .remove()
            .end()
            .append('<option value disabled selected>Silahkan Pilih</option>');
        document.getElementById('kab').value = $("#kabupaten option:selected").html();
        document.getElementById('kec').value = '';
        $.ajax({                       // initialize an AJAX request
            url: "{% url 'siswa:ajax_kecamatan' 1234%}".replace(/1234/, id),
            dataType: 'json',
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#kecamatan").attr('disabled', false);
                $.each(data.kecamatan, function (key, value) {
                    $("#kecamatan").append('<option value=' + value.id + '>' + value.nama + '</option>');
                });
            }
        });

    });

    $("#kecamatan").change(function () {
        var id = $(this).val();  // get the selected country ID from the HTML input
        $('#desa')
            .find('option')
            .remove()
            .end()
            .append('<option value disabled selected>Silahkan Pilih</option>');
        document.getElementById('kec').value = $("#kecamatan option:selected").html();
        $.ajax({                       // initialize an AJAX request
            url: "{% url 'siswa:ajax_kelurahan' 1234%}".replace(/1234/, id),
            dataType: 'json',
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#desa").attr('disabled', false);
                $.each(data.kelurahan, function (key, value) {
                    $("#desa").append('<option value=' + value.nama + '>' + value.nama + '</option>');
                });
                $("#kecamatan").append('<option value=' + key + '>' + value + '</option>');
            }
        });
    });