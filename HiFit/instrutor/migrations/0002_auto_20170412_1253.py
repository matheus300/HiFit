# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instrutor', '0001_initial'),
        ('usuario', '0001_initial'),
        ('aluno', '0002_auto_20170412_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='regra',
            name='atividade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Atividade'),
        ),
        migrations.AddField(
            model_name='regra',
            name='beneficios',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficios', to='aluno.Caracteristica'),
        ),
        migrations.AddField(
            model_name='regra',
            name='dono',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario'),
        ),
        migrations.AddField(
            model_name='regra',
            name='maleficios',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maleficios', to='aluno.Caracteristica'),
        ),
        migrations.AddField(
            model_name='regra',
            name='restricao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restricoes', to='aluno.Caracteristica'),
        ),
    ]
