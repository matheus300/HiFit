var msgNum = 0;

function enviarMensagem(aluno_selecionado) {
    $.ajax({
        url: '/usuario/chat/'+aluno_selecionado,
        method: 'GET',
        data: {
            acao: 'enviarMensagem',
            aluno_selecionado: aluno_selecionado,
            conteudo: $('#msg-input').val()
        },
        dataType: 'json',
        success: function (data) {
            msgNum++;
            $('#mensagens').append("<div id='mensagem-enviada"+msgNum+"' class='row msg_container base_sent'><div class='col-xs-10 col-md-10'><div class='messages msg_sent'><p>"+data.conteudo+"</p><time>"+data.data+"</time></div></div><div class='col-md-2 col-xs-2 avatar'><img src='/static/imagens/avatar.jpg'></div></div>");
            $("#mensagens").animate({ scrollTop: $('#mensagens').prop("scrollHeight")}, 1000);
            $('#msg-input').val('');
        }
    });
}