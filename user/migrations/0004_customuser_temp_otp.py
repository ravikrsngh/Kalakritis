# Generated by Django 4.2.5 on 2023-09-23 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_customuser_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='temp_otp',
            field=models.CharField(default='0000', max_length=4),
        ),
    ]
