# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-05 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_lorawanrawpoint_gw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lorawanrawpoint',
            name='gw',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Gateway'),
        ),
    ]
