function success(seconds) {
    const success = document.querySelector('#snackbar-success');
    success.classList.add('active');
    setTimeout(() => {
        success.classList.remove('active');
    }, seconds * 1000);
};

function error(seconds) {
    const error = document.querySelector('#snackbar-error');
    error.classList.add('active');
    setTimeout(() => {
        error.classList.remove('active');
    }, seconds * 1000);
};

function sleep(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
