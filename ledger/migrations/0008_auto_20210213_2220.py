# Generated by Django 3.1.6 on 2021-02-13 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0007_auto_20210213_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 18, 20, 28, 646461)),
        ),
    ]
