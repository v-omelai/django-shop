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
    data['items']['seller'].push({name: 'carrot', quantity: 1}, {name: 'apple', quantity: 2});
    await sendRequest(data);
}

async function cancelDeal() {
    await reloadInventory();
}

let balance = SELLER_BALANCE;
let data = {
    seller: SELLER_ID,
    buyer: BUYER_ID,
    items: {
        buyer: [],
        seller: [],
    },
}

const buttonConfirm = document.querySelector('#button-confirm');
const buttonCancel = document.querySelector('#button-cancel');

const sellerBalance = document.querySelector('#seller-balance');

const blockBuy = document.querySelector('#block-buy');
const blockBuyer = document.querySelector('#block-buyer');
const blockSell = document.querySelector('#block-sell');
const blockSeller = document.querySelector('#block-seller');

const cellEmpty = CELL_EMPTY;
const cellQuantity = CELL_QUANTITY;

//sellerBalance.innerText = `Your balance will be ${ balance } UAH`;
//blockBuy.innerHTML = cellEmpty.repeat(12);

buttonConfirm.addEventListener('click', confirmDeal);
buttonCancel.addEventListener('click', cancelDeal);
