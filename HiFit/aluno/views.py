    # -*- coding: utf-8 -*-

import re
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from utils.tipos import *
from usuario.models import *
from instrutor.models import Regra
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from instrutor.models import Regra
from django.http import JsonResponse


@login_required(login_url="/usuario/login/")
def gerenciamento_aluno(request):

    # Iniciar variaveis
    cadastro = 'completo'

    # Pega informacoes do usuario logado
    user_logado = request.user.username
    usuario = User.objects.get(username=user_logado)
    aluno_logado = Usuario.objects.get(user=usuario)
    lista_caracteristicas = [{'descricao': c.descricao, 'valor': c.valor, 'tipo': c.tipo} for c in
                             aluno_logado.caracteristicas.all()]
    lista_descricao = [d['descricao'] for d in lista_caracteristicas]
    lista_tipo = [d['tipo'] for d in lista_caracteristicas]

    # Constroi lista de acordo com o tipo
    lista_preferencias = [l for l in lista_caracteristicas if tipoCaracteristica.PREFERENCIA.value == l['tipo']]
    lista_doenca = [l for l in lista_caracteristicas if tipoCaracteristica.DOENCA.value == l['tipo']]
    lista_dificuldade_motora = [l for l in lista_caracteristicas if
                                tipoCaracteristica.DIFICULDADE_MOTORA.value == l['tipo']]

    # Cria form e preenche com valores ja cadastrados
    form = gerenciamentoAlunoForm()
    if aluno_logado.caracteristicas.all():

        # Altura
        aluno_logado_altura = aluno_logado.caracteristicas.filter(tipo=tipoCaracteristica.ALTURA.value)
        if aluno_logado_altura:
            form.fields['altura'].initial = aluno_logado_altura[0].descricao

        # Peso
        aluno_logado_peso = aluno_logado.caracteristicas.filter(tipo=tipoCaracteristica.PESO.value)
        if aluno_logado_peso:
            form.fields['peso'].initial = aluno_logado_peso[0].descricao

    if request.method == 'POST':
         ###################################################
        #                                                   #
        # Menus: Preferencia & Caracteristicas Fisiológicas #
        #                                                   #
         ###################################################

        # Salvar
        if 'salvar' in request.POST:

            # Percorre o request.POST buscando por select_field_*
            for select in request.POST:

                if re.match('select_field', select):

                    # Checa se a caracteristica nao esta cadastrada em Caracteristica
                    # caso afirmativo entao a nova caracteristica e' cadastrada e associada com o usuario
                    if request.POST[select] not in [c.descricao for c in Caracteristica.objects.all()]:

                        # Cria a cracteristica
                        caracteristica = Caracteristica(descricao=request.POST[select])
                        caracteristica.save()
                        # Salva a caracteristica do aluno
                        aluno_logado.caracteristicas.add(caracteristica)
                        messages.success(request, 'Característica \'' + request.POST[select] + '\' cadastrada com sucesso.')

                    # Checa se o usuario nao possui a caracteristica
                    # caso nao possua apenas associa a caracteristica a ele
                    # caso contrario nao faz nada
                    elif request.POST[select] not in lista_descricao:

                        # Salva a caracteristica do aluno
                        aluno_logado.caracteristicas.add(Caracteristica.objects.get(descricao=request.POST[select]))
                        messages.success(request, 'Característica \'' + request.POST[select] + '\' cadastrada com sucesso.')

            return redirect("/aluno/gerenciar")

        # Excluir
        elif 'excluir' in request.POST:

            # Caracteristica para ser deletada
            carac_del = request.POST['excluir'].replace("_", " ")

            # Checa se o que quer ser deletado ja foi criado pelo usuario
            if carac_del in lista_descricao:

                aluno_logado.caracteristicas.remove(Caracteristica.objects.get(descricao=carac_del))
                messages.success(request, 'Característica \'' + carac_del + '\' excluída com sucesso.')

            return redirect("/aluno/gerenciar")

         ##############################
        #                              #
        # Menu: Caracteristicas Física #
        #                              #
         ##############################

        form = gerenciamentoAlunoForm(request.POST)

        # Caso o form esteja valido
        if form.is_valid():

            # Caso a caracteristica altura seja nova
            if tipoCaracteristica.ALTURA.value not in lista_tipo:

                caracteristica = Caracteristica(descricao=str(form.cleaned_data.get('altura')),
                                                valor=ValorCaracteristica.ALTURA.value,
                                                tipo=tipoCaracteristica.ALTURA.value)
                caracteristica.save()
                aluno_logado.caracteristicas.add(caracteristica)

            else:
                aluno_logado.caracteristicas.filter(tipo=tipoCaracteristica.ALTURA.value).update(descricao=str(form.cleaned_data.get('altura')))

            # Caso a caracteristica peso seja nova
            if tipoCaracteristica.PESO.value not in lista_tipo:

                caracteristica = Caracteristica(descricao=str(form.cleaned_data.get('peso')),
                                                valor=ValorCaracteristica.PESO.value,
                                                tipo=tipoCaracteristica.PESO.value)
                caracteristica.save()
                aluno_logado.caracteristicas.add(caracteristica)

            else:
                aluno_logado.caracteristicas.filter(tipo=tipoCaracteristica.PESO.value).update(descricao=str(form.cleaned_data.get('peso')))

            messages.success(request, 'Característica cadastrada com sucesso.')
            return redirect("/aluno/gerenciar")


    # Checa o que o usuario já cadastrou
    if not lista_preferencias and not (tipoCaracteristica['ALTURA'].value in lista_tipo) and not (tipoCaracteristica['ALTURA'].value in lista_tipo) and not lista_doenca and not lista_dificuldade_motora:
        messages.warning(request, 'Você deve cadastrar uma preferência, todas as características físicas e uma característica fisiológica \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    elif not lista_preferencias and not (tipoCaracteristica['ALTURA'].value in lista_tipo) and not (tipoCaracteristica['ALTURA'].value in lista_tipo):
        messages.warning(request, 'Você deve cadastrar uma preferência e todas as características físicas \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    elif not lista_preferencias and not lista_doenca and not lista_dificuldade_motora:
        messages.warning(request, 'Você deve cadastrar uma preferência e uma característica fisiológica \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    elif not (tipoCaracteristica['ALTURA'].value in lista_tipo) and not (tipoCaracteristica['ALTURA'].value in lista_tipo) and not lista_doenca and not lista_dificuldade_motora:
        messages.warning(request, 'Você deve cadastrar todas as características físicas e uma característica fisiológica \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    elif not lista_preferencias:
        messages.warning(request, 'Você deve cadastrar uma preferência \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    elif not (tipoCaracteristica['ALTURA'].value in lista_tipo) and not (tipoCaracteristica['ALTURA'].value in lista_tipo):
        messages.warning(request, 'Você deve cadastrar todas as características físicas \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    elif not lista_doenca and not lista_dificuldade_motora:
        messages.warning(request, 'Você deve cadastrar uma característica fisiológica \
                         para ter acesso a outras funcionalidades.')
        cadastro = 'incompleto'
    
    context = {
        'aluno' : aluno_logado.isAluno(),
        'form': form,
        'cadastro': cadastro,
        'lista_preferencias': lista_preferencias,
        'lista_doenca': lista_doenca,
        'lista_dificuldade_motora': lista_dificuldade_motora,
        'opcoes_preferencia': CaracteristicaQualitativa.PREFERENCIA[1:],
        'opcoes_doenca': CaracteristicaQualitativa.DOENCA[1:],
        'opcoes_dificuldade_motora': CaracteristicaQualitativa.DIFICULDADE_MOTORA[1:]
    }

    return render(request, 'gerenciamento_aluno.html', context)


def calculoPontuacaoRecomendacoes(lista_preferencia_aluno, recomendacoes):

    for instrutor in recomendacoes:
        for atividade in recomendacoes[instrutor]:
            for regra in recomendacoes[instrutor][atividade]['regras']:
                if regra.beneficio in lista_preferencia_aluno:
                    recomendacoes[instrutor][atividade]['pontuacao_recomendacao'] += 1
            recomendacoes[instrutor][atividade]['pontuacao_recomendacao'] /= len(lista_preferencia_aluno)
    return recomendacoes


def calculoAvaliacaoInstrutores(recomendacoes):

    for instrutor in recomendacoes:
        for atividade in recomendacoes[instrutor]:
            if instrutor.classificacao:
                recomendacoes[instrutor][atividade]['avaliacao_instrutor'] = instrutor.classificacao.somanota

    return recomendacoes


def geraRankingTresMelhoresRecomendacoes(recomendacoes):

    lista_recomendacoes_aluno = []
    for instrutor in recomendacoes:
        lista_recomendacoes_instrutor = recomendacoes[instrutor]
        lista_recomendacoes_aluno += sorted(lista_recomendacoes_instrutor.items(),
                                            key=lambda x: x[1]['pontuacao_recomendacao'], reverse=True)

    lista_recomendacoes_aluno = sorted(lista_recomendacoes_aluno, key=lambda tup: (
    tup[1]['pontuacao_recomendacao'], tup[1]['avaliacao_instrutor']), reverse=True)

    return lista_recomendacoes_aluno[:3]


class RecomendacaoAluno:
    recomendacoes = {}


@login_required(login_url="/usuario/login/")
def buscar_recomendacoes(request):

    aluno_logado = Usuario.objects.get(user=request.user)
    aluno = aluno_logado.isAluno()

    # Pega a lista de caracteristicas do aluno
    lista_carac_aluno = aluno_logado.caracteristicas.all()
    # Lista de preferencia do aluno
    lista_preferencia_aluno = [p for p in lista_carac_aluno if p.tipo == tipoCaracteristica.PREFERENCIA.value]
    # Pega a lista de regras
    lista_regras = Regra.objects.all()
    atividades_excluidas = []

    recomendacoes = {}

    if 'buscar_recomendacoes' in request.POST:

        # Caso o aluno ja possua uma recomendacao cadastrada ele nao pode cadastrar outra
        if Recomendacao.objects.filter(aluno=aluno_logado):
            messages.warning(request, "Você já possui uma recomendação cadastrada!")
            return redirect("/aluno/buscar-recomendacoes")

        # Pega as regras que foram aceitas
        for regra in lista_regras:

            # Incrementa as atividades que o aluno nao pode fazer
            if regra.restricao in lista_carac_aluno:
                atividades_excluidas.append(regra.atividade)

            # Pega as atividades que o aluno pode fazer
            if regra.atividade not in atividades_excluidas and regra.beneficio in lista_carac_aluno:
                if regra.dono not in recomendacoes:
                    recomendacoes[regra.dono] = {regra.atividade.nome: {'regras': [], 'pontuacao_recomendacao': 0.0, 'avaliacao_instrutor': 0.0}}
                elif regra.atividade.nome not in recomendacoes[regra.dono]:
                    recomendacoes[regra.dono][regra.atividade.nome] = {'regras': [], 'pontuacao_recomendacao': 0.0, 'avaliacao_instrutor': 0.0}
                recomendacoes[regra.dono][regra.atividade.nome]['regras'].append(regra)

        # Pega as outras regras das atividades que o aluno pode fazer
        for regra in lista_regras:
            if regra.atividade.nome in recomendacoes[regra.dono]:
                if regra not in recomendacoes[regra.dono][regra.atividade.nome]['regras']:
                    recomendacoes[regra.dono][regra.atividade.nome]['regras'].append(regra)

        # Gera a ponstuacao para as recomendacoes
        recomendacoes = calculoPontuacaoRecomendacoes(lista_preferencia_aluno, recomendacoes)
        # Gera a avaliacao dos instrutores
        recomendacoes = calculoAvaliacaoInstrutores(recomendacoes)
        RecomendacaoAluno.recomendacoes = recomendacoes
        # Gera ranking das tres melhores recomendacoes
        lista_recomendacoes_aluno = geraRankingTresMelhoresRecomendacoes(recomendacoes)

        return render(request, 'buscar_recomendacoes.html', {'lista_recomendacoes_aluno': lista_recomendacoes_aluno, 'aluno': aluno})

    elif request.method == 'GET' and request.GET.get('click',0):
        recomendacao_aceita = request.GET.get('recomendacao_aceita').replace('_space_sep_', ' ')
        nome_atividade_recomendacao, username_instrutor_recomendacao = recomendacao_aceita.split('__')
        instrutor_recomendacao = Usuario.objects.filter(user=User.objects.get(username=username_instrutor_recomendacao))[0]

        #----------Criando a recomendacao
        classificacao_recomendacao = Classificacao(somanota=10, somapessoas=10)
        classificacao_recomendacao.save()
        recomendacao = Recomendacao(data=datetime.datetime.now(),
                                    classificacao=classificacao_recomendacao,
                                    atividade=Atividade.objects.get(nome=nome_atividade_recomendacao),
                                    aluno=aluno_logado,
                                    instrutor=instrutor_recomendacao)

        recomendacao.save()
        # Salvando as regras na recomendacao
        for regra in RecomendacaoAluno.recomendacoes[instrutor_recomendacao][nome_atividade_recomendacao]['regras']:
            recomendacao.regras.add(regra)

        data = {
            'value': str(request.GET.get('recomendacao_aceita'))
        }
        return JsonResponse(data)

    return render(request, 'buscar_recomendacoes.html', {'aluno': aluno})