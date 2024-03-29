# Generated by Django 4.0.1 on 2022-01-31 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0001_initial'),
        ('InventoryItems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='approver',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='Profiles.profile', verbose_name='The individual who submitted the transaction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='submitter',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='Submitter', to='Profiles.profile', verbose_name='The individual who submitted the transaction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='service_check_date',
            field=models.DateField(verbose_name='Date check was done'),
        ),
    ]
