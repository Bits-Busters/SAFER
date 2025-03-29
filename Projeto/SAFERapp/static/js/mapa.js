document.addEventListener('DOMContentLoaded', function() {
    const mapa = document.getElementById('mapa');
    const Localizacao_x = document.getElementById('id_Localizacao_x');
    const Localizacao_y = document.getElementById('id_Localizacao_y')
    mapa.addEventListener('click', function(evento) {
        // Remove qualquer ponto existente
        const pontoExistente = mapa.querySelector('.ponto');
        if (pontoExistente) {
            pontoExistente.remove();
        }


        const x = evento.offsetX;
        const y = evento.offsetY;

        const ponto = document.createElement('div');
        ponto.className = 'ponto';
        ponto.style.left = `${x}px`;
        ponto.style.top = `${y}px`;

        mapa.appendChild(ponto);

        console.log(`Coordenadas do clique - X: ${x}, Y: ${y}`);
        
        Localizacao_x.value = `${x}`
        Localizacao_y.value = `${y}`
    });
});