function habilitarEdicao() {
    // Armazenar valores originais
    document.querySelectorAll('.edit-input').forEach(input => {
        input.dataset.original = input.value;
    });

    // Alternar elementos
    document.querySelectorAll('.info-span').forEach(el => el.classList.add('d-none'));
    document.querySelectorAll('.edit-input').forEach(el => el.classList.remove('d-none'));
    
    // Alternar botões
    document.querySelector('.btnPadrao').classList.add('d-none');
    document.getElementById('confirmarEdicao').classList.remove('d-none');
    document.getElementById('cancelarEdicao').classList.remove('d-none');
}
function desabilitarEdicao() {
    console.log("cancelarEdicao() chamado");
    // Restaurar elementos
    document.querySelectorAll('.info-span').forEach(el => el.classList.remove('d-none'));
    document.querySelectorAll('.edit-input').forEach(el => {
        el.classList.add('d-none');
        // Restaurar valores originais
        if(el.dataset.original) {
            el.value = el.dataset.original;
        }
    });

    // Restaurar botões
    document.querySelector('.btnPadrao').classList.remove('d-none');
    document.getElementById('confirmarEdicao').classList.add('d-none');
    document.getElementById('cancelarEdicao').classList.add('d-none');
}