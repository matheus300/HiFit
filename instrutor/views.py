from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from utils.tipos import *
from django.http import JsonResponse
from usuario.models import Usuario
from .models import Regra
from usuario.models import Atividade
from aluno.models import Caracteristica
from django.db.models import Q      # Para fazer WHERE x=a and x=b
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime
from .utils_relatorios import *
from aluno.models import Recomendacao
from django.http import JsonResponse

#------ Mensagens do browser
# Tela Regras
msg_regra_salva = 'Regra salva com sucesso.'
msg_regra_existente = 'Regra já existe.'
msg_regra_nao_existe = 'Regra não existe.'
msg_regra_atualizada = 'Regra atualizada com sucesso.'
msg_regra_excluida = 'Regra excluída com sucesso.'
msg_regra_nao_alterada = 'Não houve alterações na regra.'
msg_permissao_concedida = 'Permissão concedida'
msg_solicitante_nao_existe = 'Usuário solicitante não existe'
msg_permissao_nao_concedida = 'Permissão não concedida'


@login_required
def cadastroInstrutor(request):
	if request.method == 'POST':
		cadastroDadosTecnicos = FormularioDadosTecnicos(request.POST)
		if cadastroDadosTecnicos.is_valid():
			instrutorLogado = Usuario.objects.get(user=request.user)
			instrutorLogado.profissao = cadastroDadosTecnicos.cleaned_data.get('profissao')
			instrutorLogado.descricao = cadastroDadosTecnicos.cleaned_data.get('dadosTecnicos')
			instrutorLogado.identificacao = cadastroDadosTecnicos.cleaned_data.get('identificacao')
			instrutorLogado.save()
			messages.success(request,"Cadastro realizado com sucesso")
			return redirect("/instrutor/regras")
		else:
			return redirect("/instrutor/cadastro")
	else:
		cadastroDadosTecnicos = FormularioDadosTecnicos()

	usuario = Usuario.objects.get(user=request.user)
	context = {
        'aluno' : usuario.isAluno(),
		'cadastro'				: True,
		'cadastroDadosTecnicos' : cadastroDadosTecnicos,
	}

	return render(request,'gerenciamento_instrutor.html',context)


@login_required
def editarCadastro(request):
	instrutorLogado = Usuario.objects.get(user=request.user)

	if request.method == 'POST':
		if "excluirCadastro" in request.POST:
			user = request.user
			logout(request)
			Usuario.objects.get(user=user).delete()
			User.objects.get(username=user.username).delete()
			return redirect("/usuario/login/")


		edicaoDadosTecnicos = FormularioEdicaoDadosTecnicos(request.POST, instance=instrutorLogado)
		if edicaoDadosTecnicos.has_changed():
			if edicaoDadosTecnicos.is_valid():
				edicaoDadosTecnicos.save()
				messages.success(request,"Alteração de dados realizada com sucesso")
			else:
				msg_identificacao_incorreta = edicaoDadosTecnicos.errors.as_text().split('*')[2]
				messages.warning(request,msg_identificacao_incorreta)
		else:
			messages.info(request,"Alteração sem mudanças, formulário idêntico ao exibido")
		return redirect("/instrutor/meu_cadastro")
	else:
		edicaoDadosTecnicos = FormularioEdicaoDadosTecnicos(instance=instrutorLogado)

	context = {
		'aluno' : instrutorLogado.isAluno(),
		'cadastro'				: False,
		'edicaoDadosTecnicos' : edicaoDadosTecnicos,
	}
	return render(request,'gerenciamento_instrutor.html',context)


# Tela de Regras
def regras(request):
    if (not request.user.is_authenticated):
        return redirect("/usuario/login")
    usuario_logado = Usuario.objects.get(user=request.user)
    atividades = Atividade.objects.all()
    restricoes = CaracteristicaQualitativa.DOENCA + CaracteristicaQualitativa.DIFICULDADE_MOTORA[1:]
    beneficios = CaracteristicaQualitativa.PREFERENCIA
    maleficios = CaracteristicaQualitativa.MALEFICIO

    # Reaproveitando algumas partes do codigo para cadastro e edicao
    if (request.method == 'POST'):

        # ----- Salvar regra
        if ("salvarRegra" in request.POST):
            # Le os campos
            atividade = request.POST['sel_cad_atividade']
            restricao = request.POST['sel_cad_restricao']
            beneficio = request.POST['sel_cad_beneficio']
            maleficio = request.POST['sel_cad_maleficio']

            # Pega os objetos referentes a cada campo
            atividade = Atividade.objects.get_or_create(nome=atividade)[0]
            if (restricao == ""):
                restricao = None
            else:
                restricao = Caracteristica.objects.get_or_create(descricao=restricao)[0]

            if (beneficio == ""):
                beneficio = None
            else:
                beneficio = Caracteristica.objects.get_or_create(descricao=beneficio)[0]

            if (maleficio == ""):
                maleficio = None
            else:
                maleficio = Caracteristica.objects.get_or_create(descricao=maleficio)[0]

            # Verifica se a regra ja existe
            if (existeRegra(Usuario.objects.get(user=usuario_logado.user), atividade, restricao, beneficio, maleficio)):
                messages.warning(request, msg_regra_existente)
            else:
                # Cria um obj
                regra_obj = Regra(atividade=atividade,
                                  restricao=restricao,
                                  beneficio=beneficio,
                                  maleficio=maleficio,
                                  dono=Usuario.objects.get(user=usuario_logado.user))
                # Salva o obj no banco de dados
                regra_obj.save()
                messages.success(request, msg_regra_salva)

        # ---------- Atualizar regra
        elif ("atualizarRegra" in request.POST):
            # Le os campos
            atividade = request.POST['sel_edit_atividade']
            restricao = request.POST['sel_edit_restricao']
            beneficio = request.POST['sel_edit_beneficio']
            maleficio = request.POST['sel_edit_maleficio']
            regra_id  = request.POST['in_edit_id']
            print(regra_id)
            # Pega os objetos referentes a cada campo
            atividade = Atividade.objects.get_or_create(nome=atividade)[0]
            if (restricao == ""):
                restricao = None
            else:
                restricao = Caracteristica.objects.get_or_create(descricao=restricao)[0]

            if (beneficio == ""):
                beneficio = None
            else:
                beneficio = Caracteristica.objects.get_or_create(descricao=beneficio)[0]

            if (maleficio == ""):
                maleficio = None
            else:
                maleficio = Caracteristica.objects.get_or_create(descricao=maleficio)[0]

            # Verifica se a regra ja existe
            if (existeRegra(Usuario.objects.get(user=usuario_logado.user), atividade, restricao, beneficio, maleficio)):
                messages.warning(request, msg_regra_existente)
            else:
                regra_anterior = Regra.objects.get(id=regra_id)
                if (atividade == regra_anterior.atividade and restricao==regra_anterior.restricao and
                             beneficio==regra_anterior.beneficio and maleficio==regra_anterior.maleficio):
                    messages.warning(request, msg_regra_nao_alterada)
                else:
                    regra_anterior.atividade=atividade
                    regra_anterior.restricao=restricao
                    regra_anterior.beneficio=beneficio
                    regra_anterior.maleficio=maleficio
                    regra_anterior.save(update_fields=['atividade', 'restricao', 'beneficio', 'maleficio'])
                    messages.success(request, msg_regra_atualizada)

        # ---------- Excluir regra
        elif("excluirRegra" in request.POST):
            regra_id = request.POST['excluirRegra']
            regra = Regra.objects.get(id=regra_id)
            if (regra):
                regra.delete()
                messages.success(request, msg_regra_excluida)
            else:
                messages.warning(request, msg_regra_nao_existe)

        # ---------- Aceitar Solicitacao
        elif ("aceitarSolicitacao" in request.POST):
            regra_id = request.POST['aceitarSolicitacao']
            regra = Regra.objects.get(id=regra_id)
            if (regra):
                usuario_solicitante = Usuario.objects.get(user=regra.solicitante.user)
                if (usuario_solicitante):
                    regra.dono = usuario_solicitante
                    regra.solicitante = None
                    regra.save(update_fields=['dono', 'solicitante'])
                    messages.success(request, msg_permissao_concedida)
                else:
                    messages.warning(request, msg_solicitante_nao_existe)
            else:
                messages.warning(request, msg_regra_nao_existe)

        # ---------- Recusar Solicitacao
        elif ("recusarSolicitacao" in request.POST):
            regra_id = request.POST['recusarSolicitacao']
            regra = Regra.objects.get(id=regra_id)
            if (regra):
                regra.solicitante = None
                regra.save(update_fields=['solicitante'])
                messages.success(request, msg_permissao_nao_concedida)
            else:
                messages.warning(request, msg_regra_nao_existe)
                    # return redirect('/instrutor/regras')
        #return redirect('/instrutor/regras')

    # ---------- Excluir regra
    elif (request.method == "GET"):
        if request.GET.get('click',0):
            instrutorLogado = Usuario.objects.get(user=User.objects.get(username=request.user.username))
            regra = Regra.objects.get(id=request.GET.get('regra_solicitada'))
            regra.solicitante = instrutorLogado
            regra.data_solicitacao = datetime.today()
            regra.save()
            data = {
              'value' : str(request.GET.get('regra_solicitada'))
            }
            return JsonResponse(data)

        #verifica quais regras ja podem ir para o solicitante

        #return redirect('/instrutor/regras')

    # Salva regras do usuário e de outros usuarios, e solicitacoes de perimissao no context
    minhas_regras = Regra.objects.filter(dono=usuario_logado)
    outras_regras = Regra.objects.exclude(dono=usuario_logado)
    solicitacoes = Regra.objects.filter(Q(solicitante__isnull=False) & Q(dono=usuario_logado))
    usuario = Usuario.objects.get(user=request.user)
    context = {
        'aluno' : usuario.isAluno(),
        'atividades': atividades,
        'restricoes': restricoes,
        'beneficios': beneficios,
        'maleficios': maleficios,
        'minhas_regras': minhas_regras,
        'outras_regras': outras_regras,
        'solicitacoes': solicitacoes
    }
    
    return render(request, 'regras.html', context)


# -----------------------------------------------
# Retorna se a regra ja esta cadastrada no banco
def existeRegra(dono, atividade, restricao, beneficio, maleficio):
    existe = list(Regra.objects.filter(Q(atividade=atividade) &
                                       Q(restricao=restricao) &
                                       Q(beneficio=beneficio) &
                                       Q(maleficio=maleficio) &
                                       Q(dono=dono)
                                       ))
    return existe

@login_required
def relatorios(request):
    instrutor_logado = Usuario.objects.get(user=request.user)
    context = {}
    if request.method == 'POST':
        dt_inicial = request.POST['dt-inicial-relatorios']
        dt_final = request.POST['dt-final-relatorios']
        tipo_relatorio = request.POST['sel-relatorios-tipo']

        dt_inicial = dt_inicial.replace("/", "")
        dt_final = dt_final.replace("/", "")

        # Valida as datas
        erros, dt_inicial_obj, dt_final_obj = validaDatas(dt_inicial, dt_final)
        if erros:
            for i in range(0, len(erros)):
                messages.warning(request, erros[i])

        else:
            acao = ""
            if "salvar-relatorios" in request.POST:
                acao = "salvar"
            elif "visualizar-relatorios" in request.POST:
                acao = "visualizar"

            # Filtra a recomendacao por instrutor e data
            recomendacoes = Recomendacao.objects.filter(Q(instrutor=instrutor_logado) & Q(data__range=(dt_inicial_obj, dt_final_obj)))

            if tipo_relatorio == "geral":
                qtd_recomendacoes = recomendacoes.count()
                media_classificacao, atividades = getComponentesRecomendacao(recomendacoes)
                context = {
                    'qtd_recomendacoes': qtd_recomendacoes,
                    'atividades': atividades,
                    'media_clasificacao': media_classificacao,
                    'tipo_relatorio': tipo_relatorio,
                    'acao': acao
                }
            elif tipo_relatorio == "aluno":
                alunos = getDadosAlunos(recomendacoes)
                context = {
                    'aluno': instrutor_logado.isAluno(),
                    'alunos': alunos,
                    'tipo_relatorio': tipo_relatorio,
                    'acao': acao,
                    'AlunoRelatorio': AlunoRelatorio
                }
    else:
        context = {'aluno': instrutor_logado.isAluno()}

    return render(request, 'relatorios.html', context)