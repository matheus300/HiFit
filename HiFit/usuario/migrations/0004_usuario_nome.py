# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-15 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20170414_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='nome',
            field=models.CharField(default='teste', max_length=100),
            preserve_default=False,
        ),
    ]