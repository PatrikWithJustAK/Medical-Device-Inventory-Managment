# Generated by Django 4.0.1 on 2022-01-31 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryItems', '0003_alter_transaction_approver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='service_check_date',
            field=models.DateField(verbose_name='Date check was done MM/DD/YYYY'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(verbose_name='When Transaction was submitted MM/DD/YY'),
        ),
    ]
