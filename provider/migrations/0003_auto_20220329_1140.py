# Generated by Django 2.2.20 on 2022-03-29 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_auto_20220326_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Providers/ImagesProducts'),
        ),
        migrations.AddField(
            model_name='provider',
            name='name_product',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
