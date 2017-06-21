# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_post_privacidade'),
        ('aluno', '0002_auto_20170412_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recomendacao',
            name='usuario',
        ),
        migrations.AddField(
            model_name='recomendacao',
            name='aluno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recomendacoes_aluno', to='usuario.Usuario'),
        ),
        migrations.AddField(
            model_name='recomendacao',
            name='atividade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Atividade'),
        ),
        migrations.AddField(
            model_name='recomendacao',
            name='instrutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recomendacoes_instrutor', to='usuario.Usuario'),
        ),
        migrations.AlterField(
            model_name='recomendacao',
            name='data',
            field=models.DateField(),
        ),
    ]