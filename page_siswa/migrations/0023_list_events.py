# Generated by Django 3.0.3 on 2020-05-07 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_siswa', '0022_auto_20200502_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='list_events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField(default=None, null=True)),
                ('end_date', models.DateField(default=None, null=True)),
            ],
        ),
    ]
