# Generated by Django 3.0.3 on 2020-05-07 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0025_auto_20200507_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_events',
            name='start_date',
            field=models.DateField(default=None),
        ),
    ]