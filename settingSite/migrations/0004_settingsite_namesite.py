# Generated by Django 2.2.20 on 2022-04-09 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settingSite', '0003_settingsite_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingsite',
            name='nameSite',
            field=models.CharField(default='allAfrik', max_length=255),
        ),
    ]
