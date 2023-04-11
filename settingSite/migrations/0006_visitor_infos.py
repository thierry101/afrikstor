# Generated by Django 2.2.20 on 2022-06-30 08:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0005_auto_20220628_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor_Infos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('page_visited', models.TextField()),
                ('event_date', models.DateTimeField(verbose_name=datetime.datetime(2022, 6, 30, 8, 28, 55, 951553, tzinfo=utc))),
            ],
        ),
    ]