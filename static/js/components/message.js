function handleMessageCheckbox() {
    localStorage.setItem('show', JSON.stringify(!this.checked));
}

function handleMessageModal() {
    const show = localStorage.getItem('show') || true;
    if (JSON.parse(show)) messageDialog.show()
}

const messageDialog = document.querySelector('#dialog-do-not-show');
const messageCheckbox = document.querySelector('#checkbox-do-not-show');

messageCheckbox.addEventListener('change', handleMessageCheckbox);

document.addEventListener('DOMContentLoaded', handleMessageModal);
