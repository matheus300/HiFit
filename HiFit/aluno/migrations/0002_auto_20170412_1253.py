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
        ('aluno', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recomendacao',
            name='classificacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Classificacao'),
        ),
        migrations.AddField(
            model_name='recomendacao',
            name='regras',
            field=models.ManyToManyField(related_name='recomendacoes', to='instrutor.Regra'),
        ),
        migrations.AddField(
            model_name='recomendacao',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomendacoes', to='usuario.Usuario'),
        ),
    ]
