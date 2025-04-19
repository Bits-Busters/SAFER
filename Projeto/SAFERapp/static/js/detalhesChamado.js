$(document).ready(function(){
    $(".popupimage").click(function(event){
        event.preventDefault();
        $(".modal img").attr("src", $(this).attr("src"));
        $(".modal").modal("show");
    });
});

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

document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-image-form');
    const formsetContainer = document.getElementById('image-formset');
    const managementForm = document.querySelector('[name="Imagens_registradas-TOTAL_FORMS"]');

    if (addButton) {
        addButton.addEventListener('click', function() {
            console.log('Add image form clicked');  // Debugging log

            // Check if managementForm exists and has a valid value
            if (!managementForm) {
                console.error('Formset TOTAL_FORMS element not found');
                return;
            }

            const totalForms = parseInt(managementForm.value);
            const newFormId = totalForms;

            // Check if there are any image forms initially
            const imageForms = formsetContainer.querySelectorAll('.image-form');
            if (imageForms.length === 0) {
                console.error('No image forms to clone');
                return;
            }

            // Clone the first image form
            const newForm = imageForms[0].cloneNode(true);
            newForm.setAttribute('data-form-id', newFormId);

            // Reset the file input field
            const imageInput = newForm.querySelector('input[type="file"]');
            imageInput.value = ''; // Reset file input value

            // Update the 'name' attributes for the cloned form
            newForm.querySelector('input[type="file"]').name = `formset-${newFormId}-Image`;

            // Add the new form to the formset container
            formsetContainer.appendChild(newForm);

            // Add event listener to remove button in the cloned form
            newForm.querySelector('.remove-image-form').addEventListener('click', function() {
                removeImageForm(newFormId);
            });

            // Update the TOTAL_FORMS field
            managementForm.value = totalForms + 1;
        });
    } else {
        console.error('Add image form button not found');
    }

    function removeImageForm(formId) {
        const formToRemove = formsetContainer.querySelector(`.image-form[data-form-id="${formId}"]`);
        if (formToRemove) {
            formsetContainer.removeChild(formToRemove);
            updateManagementForm();
        }
    }

    function updateManagementForm() {
        const forms = formsetContainer.querySelectorAll('.image-form');
        if (managementForm) {
            managementForm.value = forms.length;
        } else {
            console.error('Formset TOTAL_FORMS element not found when updating');
        }
    }
});