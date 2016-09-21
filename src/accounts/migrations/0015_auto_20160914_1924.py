# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20160804_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='connections',
            field=models.ManyToManyField(blank=True, null=True, related_name='_userprofile_connections_+', to='accounts.UserProfile'),
        ),
    ]