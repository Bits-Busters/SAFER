const socket = new WebSocket("ws://" + window.location.host + "/ws/staff/notificacoes/");

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    criarPopUpNotificacao(data.mensagem);
};

socket.onopen = function() {
    console.log('Conectado ao WebSocket');
};

socket.onerror = function(error) {
    console.error('Erro no WebSocket:', error);
};

function criarPopUpNotificacao(mensagem) {
    console.log("Criando popup")
    const popUp = document.createElement('div');
    popUp.className = 'popup-notificacao';

    const fechar = document.createElement('button');
    fechar.className = 'fechar-popup';
    fechar.textContent = 'X';
    fechar.onclick = () => popUp.remove();

    const texto = document.createElement('span');
    texto.textContent = mensagem;

    popUp.appendChild(texto);
    popUp.appendChild(fechar);
    document.body.appendChild(popUp);

};