# Generated by Django 2.2.20 on 2022-03-23 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminProduct', '0006_delete_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('statut', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/Brand')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
