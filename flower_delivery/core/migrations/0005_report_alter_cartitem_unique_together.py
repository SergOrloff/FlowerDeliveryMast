# Generated by Django 5.1.2 on 2024-10-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_sales', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_orders', models.PositiveIntegerField()),
                ('total_customers', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
