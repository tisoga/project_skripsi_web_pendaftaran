# Generated by Django 3.0.3 on 2020-04-16 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0011_auto_20200404_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='siswa',
            name='foto_akta',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AddField(
            model_name='siswa',
            name='foto_diri',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AddField(
            model_name='siswa',
            name='foto_ijazah',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]
