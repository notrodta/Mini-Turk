# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-01 09:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0037_auto_20171201_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='bid_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 8, 9, 50, 45, 791043)),
        ),
    ]