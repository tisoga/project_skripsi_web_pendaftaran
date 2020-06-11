# Generated by Django 3.0.3 on 2020-06-10 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0032_auto_20200609_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sekolah',
            name='status_pendaftaran',
            field=models.IntegerField(choices=[(0, 'Pendaftaran diBuka'), (1, 'Pendaftaran diTutup')], default=0),
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='tabel_user',
        ),
    ]