# Generated by Django 3.1.3 on 2020-11-28 03:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20201127_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='account_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='active',
            field=models.CharField(default='False', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_of_next_payout',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='earning_balance',
            field=models.IntegerField(default=0),
        ),
    ]
