# Generated by Django 2.2.20 on 2022-08-20 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerProduct', '0009_alter_registerproduct_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerproduct',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]