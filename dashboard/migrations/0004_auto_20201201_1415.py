# Generated by Django 3.1.3 on 2020-12-01 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_invoice_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
