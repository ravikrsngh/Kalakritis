# Generated by Django 4.2.5 on 2023-10-03 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_cart_cost_price_remove_cart_selling_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='color',
            field=models.CharField(max_length=50),
        ),
    ]
