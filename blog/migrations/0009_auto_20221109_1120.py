# Generated by Django 2.2.20 on 2022-11-09 11:20

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20220820_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelblog',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, size=[500, 300], upload_to='Images/BlogCover'),
        ),
    ]