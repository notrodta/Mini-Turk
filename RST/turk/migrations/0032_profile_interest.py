# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 06:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0031_remove_profile_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interest',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
