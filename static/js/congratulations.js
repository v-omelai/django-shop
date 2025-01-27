function showSparkles(seconds) {
    function wrapper() {
        function _showSparkles() {
            party.sparkles(document.body, {
                count: party.variation.range(40, 60),
                spread: 360,
            });
        }
        _showSparkles();
        setInterval(_showSparkles, seconds * 1000);
    }
    return wrapper
}

async function createGame() {
    localStorage.removeItem('link');
    window.success(3);
    await window.sleep(4);
    window.location.href = LOADING_URL;
}

const buttonCreateGame = document.querySelector('#create-game');
buttonCreateGame.addEventListener('click', createGame);
document.addEventListener('DOMContentLoaded', showSparkles(1));
