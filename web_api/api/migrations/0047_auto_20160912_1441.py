# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-12 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_userext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='api_key',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='node',
            name='nodetype',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='api.NodeType'),
            preserve_default=False,
        ),
    ]