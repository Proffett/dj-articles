# Generated by Django 2.2.4 on 2019-11-16 20:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20191116_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 20, 59, 35, 520508, tzinfo=utc), verbose_name='date'),
        ),
    ]
