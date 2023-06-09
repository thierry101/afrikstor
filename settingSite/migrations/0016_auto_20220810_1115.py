# Generated by Django 3.2.12 on 2022-08-10 11:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0015_auto_20220809_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confidentialityandrule',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='settingsite',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visitor_infos',
            name='event_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 8, 10, 11, 15, 58, 697678, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visitor_infos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
