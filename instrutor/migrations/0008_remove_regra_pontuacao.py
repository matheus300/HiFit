# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instrutor', '0007_regra_data_solicitacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regra',
            name='pontuacao',
        ),
    ]
