# Generated by Django 4.0.5 on 2022-06-11 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='subscription',
        ),
    ]
