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

document.addEventListener('DOMContentLoaded', showSparkles(1));
