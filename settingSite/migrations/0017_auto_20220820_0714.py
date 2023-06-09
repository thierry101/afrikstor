# Generated by Django 2.2.20 on 2022-08-20 07:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0016_auto_20220810_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confidentialityandrule',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='settingsite',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='visitor_infos',
            name='event_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 8, 20, 7, 14, 8, 993582, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visitor_infos',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
