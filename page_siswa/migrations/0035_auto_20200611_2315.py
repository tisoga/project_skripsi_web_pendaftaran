# Generated by Django 3.0.3 on 2020-06-11 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0034_auto_20200611_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sekolah',
            name='status_pendaftaran',
            field=models.SmallIntegerField(choices=[(0, 'Pendaftaran diBuka'), (1, 'Pendaftaran diTutup')], default=0),
        ),
    ]
