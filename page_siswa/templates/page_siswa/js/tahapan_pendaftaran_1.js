$(document).ready(function () {
    $.ajax({
        url: "http://dev.farizdotid.com/api/daerahindonesia/provinsi",
        dataType: 'json',
        success: function (data) {
            // alert(data)
            $("#provinsi").attr('disabled', false);
            $.each(data.semuaprovinsi, function (key, value) {
                $("#provinsi").append('<option value=' + value.id + '>' + value.nama + '</option>');
            });
            $("#provinsi").append('<option value=' + key + '>' + value + '</option>');
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
        url: "http://dev.farizdotid.com/api/daerahindonesia/provinsi/" + id + "/kabupaten",
        dataType: 'json',
        success: function (data) {   // `data` is the return of the `load_cities` view function
            // alert(data.kabupatens)
            $("#kabupaten").attr('disabled', false);
            $.each(data.kabupatens, function (key, value) {
                $("#kabupaten").append('<option value=' + value.id + '>' + value.nama + '</option>');
            });
            $("#kabupaten").append('<option value=' + key + '>' + value + '</option>');
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
            url: "http://dev.farizdotid.com/api/daerahindonesia/provinsi/kabupaten/" + id + "/kecamatan",
            dataType: 'json',
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#kecamatan").attr('disabled', false);
                $.each(data.kecamatans, function (key, value) {
                    $("#kecamatan").append('<option value=' + value.id + '>' + value.nama + '</option>');
                });
                $("#kecamatan").append('<option value=' + key + '>' + value + '</option>');
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
            url: "http://dev.farizdotid.com/api/daerahindonesia/provinsi/kabupaten/kecamatan/" + id + "/desa",
            dataType: 'json',
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#desa").attr('disabled', false);
                $.each(data.desas, function (key, value) {
                    $("#desa").append('<option value=' + value.nama + '>' + value.nama + '</option>');
                });
                $("#kecamatan").append('<option value=' + key + '>' + value + '</option>');
            }
        });
    });