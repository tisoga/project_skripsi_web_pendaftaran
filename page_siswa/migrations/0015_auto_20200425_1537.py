# Generated by Django 3.0.3 on 2020-04-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0014_auto_20200416_0932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siswa',
            old_name='foto_akta',
            new_name='berkas_akta',
        ),
        migrations.RenameField(
            model_name='siswa',
            old_name='foto_ijazah',
            new_name='berkas_ijazah',
        ),
        migrations.RenameField(
            model_name='siswa',
            old_name='nilai_un_indonesia',
            new_name='nilai_indonesia',
        ),
        migrations.RenameField(
            model_name='siswa',
            old_name='nilai_un_inggris',
            new_name='nilai_inggris',
        ),
        migrations.RenameField(
            model_name='siswa',
            old_name='nilai_un_matematika',
            new_name='nilai_ipa',
        ),
        migrations.AddField(
            model_name='siswa',
            name='asal_sekolah',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='berkas_kesehatan',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='siswa',
            name='nilai_matematika',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
