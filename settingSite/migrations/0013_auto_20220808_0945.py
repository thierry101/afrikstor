# Generated by Django 2.2.20 on 2022-08-08 09:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0012_auto_20220803_0857'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OtherSetting',
        ),
        migrations.AlterField(
            model_name='visitor_infos',
            name='event_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 8, 8, 9, 45, 58, 415326, tzinfo=utc)),
        ),
    ]
