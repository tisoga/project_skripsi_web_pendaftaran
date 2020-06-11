# Generated by Django 3.0.3 on 2020-06-09 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0030_auto_20200525_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='jenis_kelamin',
            field=models.CharField(choices=[('L', 'Laki-Laki'), ('P', 'Perempuan')], default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pelengkapan Identias Diri'), (1, 'Pelengkapan Berkas-Berkas'), (2, 'Pengajuan Pendaftaran'), (3, 'Sedang Diverifikasi'), (4, 'Verifikasi Gagal'), (5, 'Proses Daftar Ulang'), (6, 'Proses Seleksi Siswa'), (7, 'Tidak Diterima'), (8, 'Diterima'), (9, 'Pendaftaran ditutup')], default=0, null=True),
        ),
    ]