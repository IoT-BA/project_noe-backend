# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-21 20:38
from __future__ import unicode_literals

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0101_gateway_last_seen_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='serial',
            field=models.CharField(blank=True, default=api.models.generate_gw_serial, max_length=16),
        ),
    ]
