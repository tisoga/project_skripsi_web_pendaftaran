# Generated by Django 3.0.3 on 2020-05-02 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0021_auto_20200502_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='nilai_indonesia',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='nilai_inggris',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='nilai_ipa',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='nilai_matematika',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=4, null=True),
        ),
    ]
