# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-08 09:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0095_auto_20161208_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='admins',
        ),
        migrations.AddField(
            model_name='node',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='node',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
