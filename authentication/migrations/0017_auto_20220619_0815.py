# Generated by Django 2.2.20 on 2022-06-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_activationcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='accountMoney',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]