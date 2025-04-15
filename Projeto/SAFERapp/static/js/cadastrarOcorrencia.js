// Inicialize o mapa
// Definindo os limites geográficos
var maxBounds = [[-8.032416227691224, -34.96295787378685], [-8.008066751036676, -34.937476728609184]]; // Região permitida
var currentMarker = null; // Variável para armazenar o marcador atual
// Inicializando o mapa
var map = L.map('map', {
    center: [-8.017598865420956, -34.94933404268544], // Centro inicial
    zoom: 15,
    maxBounds: maxBounds,
});

// Adiciona a camada de mapa (a base, usando o OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    detectRetina: true
}).addTo(map);

// Evento de clique no mapa
map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // Se já houver um marcador, remova-o
    if (currentMarker) {
        map.removeLayer(currentMarker);
    }

    // Adiciona o novo marcador
    currentMarker = L.marker([lat, lng]).addTo(map)
        .bindPopup("Você clicou aqui!")
        .openPopup();
    // Atualiza os campos ocultos com as novas coordenadas
    document.getElementById('id_Localizacao_x').value = lat;
    document.getElementById('id_Localizacao_y').value = lng;
});    
function updateProgressIndicator(pageNumber) {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        if (index < pageNumber) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

function navigatePage(pageNumber) {
    const pages = document.querySelectorAll('.page');

    // Verifica se a página 2 está sendo ativada
    if (pageNumber === 2) {
        // Espera um tempo curto para garantir que o DOM foi renderizado
        setTimeout(function() {
            // Verifica se o mapa existe antes de chamar invalidateSize
            if (typeof map !== 'undefined') {
                map.invalidateSize(); // Ajusta o mapa após a renderização da página 2
            }
        }, 100);  // 100 ms para garantir o tempo de renderização
    }

    // Validação e navegação para outras páginas
    if (pageNumber > 1) {
        const currentPage = document.querySelector('.page.active');
        const invalidFields = currentPage.querySelectorAll(':invalid');
        if (invalidFields.length > 0) {
            invalidFields[0].focus();
            invalidFields.forEach(field => {
                field.classList.add('is-invalid');
                let errorElement = document.createElement('div');
                errorElement.className = 'invalid-feedback';
                errorElement.innerText = field.validationMessage;
                if (!field.nextElementSibling) {
                    field.insertAdjacentElement('afterend', errorElement);
                }
            });
            return;
        }
    }

    // Esconde todas as páginas e mostra a página escolhida
    pages.forEach(page => page.classList.remove('active'));
    document.getElementById('page' + pageNumber).classList.add('active');

    updateProgressIndicator(pageNumber);
}

function handleSubmit(event) {
    event.preventDefault();

    const submitButton = event.target;
    const originalText = submitButton.innerHTML; // Guarda o HTML original
    submitButton.classList.add('loading');
    submitButton.innerHTML = originalText; // Mantém o texto original
    submitButton.disabled = true;

    const form = document.getElementById('form_ocorrencia');
    const currentPage = document.querySelector('.page.active');
    const invalidFields = currentPage.querySelectorAll(':invalid');

    if (invalidFields.length > 0) {
        invalidFields[0].focus();
        invalidFields.forEach(field => {
            field.classList.add('is-invalid');
            let errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            errorElement.innerText = field.validationMessage;
            if (!field.nextElementSibling) {
                field.insertAdjacentElement('afterend', errorElement);
            }
        });

        // Remove animação
        submitButton.classList.remove('loading');
        submitButton.disabled = false;
        submitButton.innerHTML = originalText; // Restaura o texto
        return;
    }
    

    // Usando fetch para enviar o formulário via AJAX
    const formData = new FormData(form);
    console.log('Form Data:', formData);  // Log para depuração

    fetch(form.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            submitButton.textContent = 'Sucesso!';
            setTimeout(() => {
                window.location.href = data.redirect_url;
            }, 1000);
        } else {
            submitButton.classList.remove('loading');
            submitButton.textContent = originalText;
            submitButton.disabled = false;
            alert('Erro: ' + data.errors.join('\n'));
        }
    })
    .catch(error => {
        console.error('Erro ao enviar o formulário:', error);
        submitButton.classList.remove('loading');
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        alert('Ocorreu um erro ao enviar o formulário.');
    });
}
document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-image-form');
    const formsetContainer = document.getElementById('image-formset');
    const managementForm = document.querySelector('[name="Imagens_registradas-TOTAL_FORMS"]');

    if (addButton) {
        addButton.addEventListener('click', function() {
            console.log('Add image form clicked');  // Log para debugging

            // Verificar se o TOTAL_FORMS está presente
            if (!managementForm) {
                console.error('Formset TOTAL_FORMS element not found');
                return;
            }

            const totalForms = parseInt(managementForm.value);  // Pega o número total de formulários
            const newFormId = totalForms;  // O novo ID do formulário será igual ao número total de formulários

            // Verificar se há formulários de imagem para clonar
            const imageForms = formsetContainer.querySelectorAll('.image-form');
            if (imageForms.length === 0) {
                console.error('No image forms to clone');
                return;
            }

            // Clonar o primeiro formulário de imagem
            const newForm = imageForms[0].cloneNode(true);
            newForm.setAttribute('data-form-id', newFormId);  // Atribui um novo ID ao formulário clonado

            // Resetar o campo de entrada de imagem
            const imageInput = newForm.querySelector('input[type="file"]');
            imageInput.value = '';  // Reseta o valor do campo de entrada de arquivo

            // Atualizar o atributo 'name' para que ele siga a estrutura do formset
            newForm.querySelector('input[type="file"]').name = `formset-${newFormId}-Image`;

            // Adicionar o novo formulário à lista
            formsetContainer.appendChild(newForm);

            // Adicionar evento de remoção ao novo formulário
            newForm.querySelector('.remove-image-form').addEventListener('click', function() {
                removeImageForm(newFormId);
            });

            // Atualizar o campo TOTAL_FORMS para refletir o novo número total de formulários
            managementForm.value = totalForms + 1;
        });
    } else {
        console.error('Add image form button not found');
    }

    function removeImageForm(formId) {
        const formToRemove = formsetContainer.querySelector(`.image-form[data-form-id="${formId}"]`);
        if (formToRemove) {
            formsetContainer.removeChild(formToRemove);
            updateManagementForm();  // Atualizar o número total de formulários
        }
    }

    function updateManagementForm() {
        const forms = formsetContainer.querySelectorAll('.image-form');
        if (managementForm) {
            managementForm.value = forms.length;  // Atualiza o valor de TOTAL_FORMS
        } else {
            console.error('Formset TOTAL_FORMS element not found when updating');
        }
    }
});