# Generated by Django 3.1.6 on 2021-02-16 20:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0020_auto_20210216_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 16, 20, 56, 16, 88484)),
        ),
    ]
