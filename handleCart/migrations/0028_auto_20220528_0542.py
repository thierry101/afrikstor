# Generated by Django 2.2.20 on 2022-05-28 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('handleCart', '0027_merge_20220521_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='infoAnonUser',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='handleCart.ShippingAdress'),
        ),
    ]
