# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0025_bidder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Temporary', max_length=9),
        ),
    ]
