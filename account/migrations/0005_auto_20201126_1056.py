# Generated by Django 3.1.3 on 2020-11-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_userprofile_referred_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_type',
            field=models.CharField(choices=[('account', 'Platium')], default='None', max_length=50),
        ),
    ]
