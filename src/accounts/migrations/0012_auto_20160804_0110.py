# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 01:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_userprofile_connections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='static/img/avatar-dhg.png', upload_to='images/profile'),
        ),
    ]
