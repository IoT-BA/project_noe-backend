# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-05 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20161005_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='lorawan_application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.LoRaWANApplication'),
        ),
    ]
