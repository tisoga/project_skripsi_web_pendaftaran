# Generated by Django 3.0.3 on 2020-04-03 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0006_siswa'),
    ]

    operations = [
        migrations.AddField(
            model_name='siswa',
            name='nis',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterModelTable(
            name='siswa',
            table='tabel_siswa',
        ),
    ]
