# Generated by Django 3.2.12 on 2022-08-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0002_advert_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]