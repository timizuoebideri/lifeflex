# Generated by Django 3.1.3 on 2020-11-28 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='method_of_payment',
            field=models.CharField(default='None', max_length=50),
        ),
    ]