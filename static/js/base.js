function success() {
    const success = document.querySelector('#snackbar-success');
    success.classList.add('active');
    setTimeout(() => {
        success.classList.remove('active');
    }, 3000);
};

function error() {
    const error = document.querySelector('#snackbar-error');
    error.classList.add('active');
    setTimeout(() => {
        error.classList.remove('active');
    }, 3000);
};
