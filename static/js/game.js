function handleMessageCheckbox() {
    localStorage.setItem('show', JSON.stringify(!this.checked));
}

function handleMessageButton() {
    messageDialog.close();
}

function handleMessageModal() {
    const show = localStorage.getItem('show') || true;
    if (JSON.parse(show)) messageDialog.show()
}

const messageDialog = document.querySelector('#dialog-do-not-show');
const messageCheckbox = document.querySelector('#checkbox-do-not-show');
const messageButton = document.querySelector('#button-do-not-show');

messageCheckbox.addEventListener('change', handleMessageCheckbox);
messageButton.addEventListener('click', handleMessageButton);

document.addEventListener('DOMContentLoaded', handleMessageModal);
