# Generated by Django 2.2.20 on 2022-04-30 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handleCart', '0005_auto_20220430_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='handleCart.OrderItem'),
        ),
    ]
