# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-04 12:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_node_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='responsible',
        ),
    ]
