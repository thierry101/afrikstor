# Generated by Django 2.2.20 on 2022-10-12 13:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0022_auto_20221011_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor_infos',
            name='event_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 10, 12, 13, 39, 13, 50845, tzinfo=utc)),
        ),
    ]
