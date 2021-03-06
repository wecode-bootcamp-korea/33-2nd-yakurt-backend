# Generated by Django 4.0.5 on 2022-06-09 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_subscribing', models.BooleanField(default=True)),
                ('delivery_message', models.CharField(max_length=100)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscription')),
            ],
            options={
                'db_table': 'subscription_items',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=1000)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
    ]
