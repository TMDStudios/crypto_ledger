# Generated by Django 3.1.6 on 2022-12-21 03:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dark_mode',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='limit_history',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='transaction_view',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='date',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 3, 13, 30, 97510)),
        ),
    ]