# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20160628_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='for_doctor',
            field=models.BooleanField(default=True),
        ),
    ]
