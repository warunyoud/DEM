# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20160801_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(null=True, upload_to='images/profile'),
        ),
    ]
