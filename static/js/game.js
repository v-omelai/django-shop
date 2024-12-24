function handleCheckbox() {
    localStorage.setItem('show', JSON.stringify(!this.checked));
}

function handleButton() {
    dialog.close();
}

function handleModal() {
    const show = localStorage.getItem('show') || true;
    if (JSON.parse(show)) dialog.show()
}

const dialog = document.querySelector('#dialog-do-not-show');
const checkbox = document.querySelector('#checkbox-do-not-show');
const button = document.querySelector('#button-do-not-show');

checkbox.addEventListener('change', handleCheckbox);
button.addEventListener('click', handleButton);

document.addEventListener('DOMContentLoaded', handleModal);
