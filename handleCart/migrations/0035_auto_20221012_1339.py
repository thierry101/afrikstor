# Generated by Django 2.2.20 on 2022-10-12 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('handleCart', '0034_auto_20220820_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='handleCart.ShippingAdress'),
        ),
    ]
