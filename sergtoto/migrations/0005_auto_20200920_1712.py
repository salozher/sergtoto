# Generated by Django 3.0.7 on 2020-09-20 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sergtoto', '0004_auto_20200920_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_date_time',
            field=models.DateTimeField(default=datetime.time(15, 12, 26, 612240)),
        ),
    ]