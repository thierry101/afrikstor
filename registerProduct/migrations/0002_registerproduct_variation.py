# Generated by Django 2.2.20 on 2022-03-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerProduct', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerproduct',
            name='variation',
            field=models.BooleanField(default=False),
        ),
    ]
