function mostrarAtualizacao() {
    document.getElementById("divAtualizacao").style.display = "block"; // Mostra a div
    document.getElementById("btnMostrar").style.display = "none"; // Esconde o botão "Atualizar"
}

function fecharAtualizacao() {
    document.getElementById("divAtualizacao").style.display = "none"; // Esconde a div
    document.getElementById("btnMostrar").style.display = "inline-block"; // Mostra o botão "Atualizar" de novo
}

function editarObservacao(id, corpo) {
    document.getElementById("observacao_id").value = id;
    document.getElementById("id_corpo").value = corpo; // Corrigido para preencher corretamente o campo de texto
    document.getElementById("form_type").value = "editar_observacao";

    document.getElementById("titulo-form").innerText = "Editar Observação"; 
    document.getElementById("botao-form").innerText = "Atualizar"; 

    document.getElementById("cancelar-edicao").style.display = "inline"; // Exibe o botão de cancelar
}

function cancelarEdicao() {
    document.getElementById("observacao_id").value = "";
    document.getElementById("id_corpo").value = "";
    document.getElementById("form_type").value = "adicionar_observacao";

    document.getElementById("titulo-form").innerText = "Adicionar Observação"; 
    document.getElementById("botao-form").innerText = "Salvar"; 

    document.getElementById("cancelar-edicao").style.display = "none"; // Esconde o botão de cancelar
}