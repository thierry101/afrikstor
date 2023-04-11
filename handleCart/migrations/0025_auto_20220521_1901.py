# Generated by Django 2.2.20 on 2022-05-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleCart', '0024_auto_20220521_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, to='handleCart.OrderItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
