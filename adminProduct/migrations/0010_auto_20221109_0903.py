# Generated by Django 2.2.20 on 2022-11-09 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminProduct', '0009_auto_20220820_0714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='image',
            new_name='imageBrand',
        ),
    ]