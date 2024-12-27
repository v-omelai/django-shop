async function initiateGame() {
    try {
        let parsed;
        let link = localStorage.getItem('link');
        if (link) {
            parsed = JSON.parse(link);
            const response = await fetch(parsed);
            if (response.status == 404) {
                console.log(`Not Found: ${link}`);
                localStorage.removeItem('link');
                await initiateGame();
                return;
            }
        } else {
            const response = await fetch(API_CREATE_SELLER_URL, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                const json = await response.json();
                parsed = json.link;
                link = JSON.stringify(parsed);
                localStorage.setItem('link', link);
                console.log(`Created: ${link}`);
            } else {
                throw new Error(response.status);
            }
        }
        window.success(3);
        await window.sleep(4);
        window.location.href = parsed;
    } catch (error) {
        console.error(error.message);
        window.error(3);
    }
}

document.addEventListener('DOMContentLoaded', initiateGame);
