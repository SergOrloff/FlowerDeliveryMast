# Generated by Django 5.1.2 on 2024-10-25 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('roses', 'Розы'), ('tulips', 'Тюльпаны'), ('orchids', 'Орхидеи'), ('bouquets', 'Букеты'), ('other', 'Другие')], default='roses', max_length=50),
        ),
    ]
