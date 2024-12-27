function handleCroppie(e) {
    croppieInstance.bind({
        url: e.target.result
    });
}

function handleSettingsImage(e) {
    if (!croppieInstance) {
        croppieInstance = new Croppie(croppieContainer, {
            viewport: { width: 200, height: 200, type: 'circle' },
            boundary: { width: 300, height: 300 },
            showZoomer: true
        });
    };

    const file = e.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.addEventListener('load', handleCroppie);
        reader.readAsDataURL(file);
    };
}

async function handleSettingsButton() {
    try {
        let data = {};
        if (settingsText.value !== '') data['name'] = settingsText.value;
        if (croppieInstance) {
            await croppieInstance.result({
                type: 'base64',
                format: 'jpeg',
                circle: false,
            }).then((image) => {
                data['image'] = image;
            });
        };
        const response = await fetch(API_UPDATE_SELLER_URL, {
            method: 'PATCH',
            headers: {
                'X-CSRFToken': window.getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            const json = await response.json();
            sellerName.innerText = `${json.name} (You)`;
            sellerNameHelper.innerText = `Your name: ${json.name}`;
            sellerImage.src = sellerImageHelper.src = json.image;
        } else {
            throw new Error(response.status);
        };
        window.success(3);
    } catch (error) {
        console.error(error.message);
        window.error(3);
    }
}

const settingsDialog = document.querySelector('#dialog-settings');
const settingsText = document.querySelector('#text-settings');
const settingsImage = document.querySelector('#image-settings');
const settingsButton = document.querySelector('#button-settings');

const sellerName = document.querySelector('#seller-name');
const sellerImage = document.querySelector('#seller-image');
const sellerNameHelper = document.querySelector('#seller-name-helper');
const sellerImageHelper = document.querySelector('#seller-image-helper');

const croppieContainer = document.querySelector('#croppie-container');

let croppieInstance;

settingsImage.addEventListener('change', handleSettingsImage);
settingsButton.addEventListener('click', handleSettingsButton);
