# Generated by Django 4.2.5 on 2023-09-25 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_temp_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='receive_sms_notitication',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='address_type',
            field=models.CharField(choices=[('1', 'Home'), ('2', 'Office'), ('3', 'Others')], default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='country',
            field=models.CharField(default='India', max_length=30),
        ),
    ]