# Generated by Django 3.2.12 on 2023-03-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0006_auto_20221109_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
