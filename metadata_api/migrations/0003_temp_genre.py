# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-06 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata_api', '0002_auto_20160806_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp',
            name='genre',
            field=models.CharField(default='', max_length=50),
        ),
    ]
