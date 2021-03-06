# Generated by Django 3.0.3 on 2020-07-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0045_auto_20200729_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='sekolah',
            name='alamat_lengkap',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='sekolah',
            name='status_pendaftaran',
            field=models.IntegerField(choices=[(0, 'Pendaftaran ditutup'), (1, 'Pendaftaran dibuka'), (2, 'Proses Seleksi'), (3, 'Proses Daftar Ulang'), (4, 'Pengumuman')], default=1),
        ),
    ]
