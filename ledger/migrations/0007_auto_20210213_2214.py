# Generated by Django 3.1.6 on 2021-02-13 18:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0006_auto_20210213_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 18, 14, 42, 635557)),
        ),
    ]
