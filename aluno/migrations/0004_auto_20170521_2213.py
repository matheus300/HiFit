# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-22 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0003_auto_20170521_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recomendacao',
            name='data',
            field=models.DateField(),
        ),
    ]