async function initiateGame() {
    try {
        const response = await fetch('/api/game/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        });
        if (response.ok) {
            const json = await response.json();
            window.success(3);
            await window.sleep(4);
            window.location.href = json.redirect;
        } else {
            throw new Error(response.status);
        }
    } catch (error) {
        console.error(error.message);
        window.error(3);
    }
}

document.addEventListener('DOMContentLoaded', initiateGame);
