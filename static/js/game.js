async function reloadInventory() {
    window.location.reload();
}

async function sendRequest(data) {
    try {
        const response = await fetch(API_CREATE_TRANSACTION_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(response.status);
        window.success(3);
        await window.sleep(4);
        await reloadInventory();
    } catch (error) {
        console.error(error.message);
        window.error(3);
    }
}

async function confirmDeal() {
    data['items']['seller'].push({name: 'carrot', quantity: 1}, {name: 'apple', quantity: 1});
    await sendRequest(data);
}

async function cancelDeal() {
    await reloadInventory();
}

let data = {
    seller: API_SELLER_ID,
    buyer: API_BUYER_ID,
    items: {
        buyer: [],
        seller: [],
    },
}

const buttonConfirm = document.querySelector('#button-confirm');
const buttonCancel = document.querySelector('#button-cancel');

buttonConfirm.addEventListener('click', confirmDeal);
buttonCancel.addEventListener('click', cancelDeal);
