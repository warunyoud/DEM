# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 03:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20160627_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='my_doctors',
            field=models.ManyToManyField(related_name='my_clients', to=settings.AUTH_USER_MODEL),
        ),
    ]