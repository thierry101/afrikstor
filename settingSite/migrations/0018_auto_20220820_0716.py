# Generated by Django 2.2.20 on 2022-08-20 07:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0017_auto_20220820_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor_infos',
            name='event_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 8, 20, 7, 16, 25, 610788, tzinfo=utc)),
        ),
    ]