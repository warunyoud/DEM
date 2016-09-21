# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160801_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='connections',
            field=models.ManyToManyField(related_name='_userprofile_connections_+', to='accounts.UserProfile'),
        ),
    ]