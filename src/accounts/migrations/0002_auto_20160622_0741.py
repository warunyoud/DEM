# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 07:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='user_profile',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='user_profile',
            new_name='profile',
        ),
    ]
