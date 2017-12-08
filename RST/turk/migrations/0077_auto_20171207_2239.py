# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 22:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0076_auto_20171207_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='bid_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 22, 39, 40, 915390)),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 28, 22, 39, 40, 915447)),
        ),
        migrations.AlterField(
            model_name='jobsubmission',
            name='submission',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='acc_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 7, 22, 39, 40, 912779)),
        ),
    ]