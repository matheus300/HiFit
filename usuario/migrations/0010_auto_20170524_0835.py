# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_post_privacidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='seguidores',
            field=models.ManyToManyField(blank=True, related_name='seguidopor', to='usuario.Usuario'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='seguindo',
            field=models.ManyToManyField(blank=True, related_name='segue', to='usuario.Usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='caracteristicas',
            field=models.ManyToManyField(blank=True, to='aluno.Caracteristica'),
        ),
    ]