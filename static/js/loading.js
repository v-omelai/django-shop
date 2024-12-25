async function initiateGame() {
    try {
        let redirect = localStorage.getItem('redirect');
        if (redirect) {
            console.log(`Found: ${redirect}`);
        } else {
            const response = await fetch('/api/game/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                const json = await response.json();
                redirect = JSON.stringify(json.redirect);
                localStorage.setItem('redirect', redirect);
                console.log(`Created: ${redirect}`);
            } else {
                throw new Error(response.status);
            }
        }
        window.success(3);
        await window.sleep(4);
        window.location.href = JSON.parse(redirect);
    } catch (error) {
        console.error(error.message);
        window.error(3);
    }
}

document.addEventListener('DOMContentLoaded', initiateGame);
