# Generated by Django 3.0.7 on 2020-09-27 09:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sergtoto', '0005_auto_20200920_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_date_time',
            field=models.DateTimeField(default=datetime.time(9, 34, 7, 157079)),
        ),
    ]
