# Generated by Django 3.1.3 on 2020-12-01 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_invoice_method_of_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='comment',
            field=models.CharField(default='', max_length=500),
        ),
    ]
