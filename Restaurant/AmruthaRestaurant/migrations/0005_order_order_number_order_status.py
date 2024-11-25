# Generated by Django 5.1.2 on 2024-11-01 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmruthaRestaurant', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('processing', 'Processing'), ('delivered', 'Delivered')], default='ordered', max_length=20),
        ),
    ]
