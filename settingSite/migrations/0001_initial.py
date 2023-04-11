# Generated by Django 2.2.20 on 2022-03-26 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SettingSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('localisation', models.CharField(blank=True, max_length=255, null=True)),
                ('link_whatsapp', models.CharField(blank=True, max_length=255, null=True)),
                ('link_facebook', models.CharField(blank=True, max_length=255, null=True)),
                ('link_messenger', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='Images/SettingSites')),
                ('fav_icon', models.ImageField(blank=True, null=True, upload_to='Images/SettingSites')),
            ],
        ),
    ]