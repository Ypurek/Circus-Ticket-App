# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 19:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20170918_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='bought',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]