# Generated by Django 2.2.20 on 2022-05-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactAndAbout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagecontact',
            name='statut',
            field=models.CharField(default='non lu', max_length=15),
        ),
    ]