# Generated by Django 3.1.6 on 2021-02-17 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0024_auto_20210217_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 17, 18, 29, 9, 525386)),
        ),
    ]
