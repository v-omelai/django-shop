const initiateGame = () => {
    success();
//    error();
    let player = JSON.parse(localStorage.getItem('player'));
    if (player) {
        console.log(player);
    } else {
        console.log(player);
    };
};

document.addEventListener('DOMContentLoaded', initiateGame);
