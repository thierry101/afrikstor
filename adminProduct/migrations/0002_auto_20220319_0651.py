# Generated by Django 2.2.20 on 2022-03-19 06:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminProduct', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='statut',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='statut',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
