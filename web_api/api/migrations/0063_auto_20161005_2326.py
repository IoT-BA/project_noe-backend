# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-05 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_node_lorawan_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='lorawan_ASK',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='lorawan_DevAddr',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='lorawan_DevEUI',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='lorawan_NSK',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]