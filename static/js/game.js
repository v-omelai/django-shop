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

async function reloadInventory() {
    window.location.reload();
}

async function confirmDeal() {
    await sendRequest(data);
}

async function cancelDeal() {
    await reloadInventory();
}

async function handleButtons() {
    if (balanceCurrent === balanceGoal) buttonConfirm.removeAttribute('disabled')
    else buttonConfirm.setAttribute('disabled', 'disabled');
    if (balanceCurrent === balanceInitial) buttonCancel.setAttribute('disabled', 'disabled')
    else buttonCancel.removeAttribute('disabled');
}

async function handleLeftBlock(item, items, operator, rightBlock) {
    const cloned = item.cloneNode(true);
    const itemBadge = item.querySelector('.quantity');
    const clonedBadge = cloned.querySelector('.quantity');
    const quantity = parseInt(item.dataset.quantity);
    const name = item.dataset.name;
    const nameLower = name.toLowerCase();
    const price = parseInt(item.dataset.price);
    const index = items.findIndex(item => item.name === nameLower);

    // Left block

    if (quantity === 1) {
        item.outerHTML = cellEmpty;
    } else if (quantity === 2) {
        if (itemBadge) itemBadge.remove();
        item.dataset.quantity = 1;
    } else {
        if (itemBadge) itemBadge.innerText = quantity - 1;
        item.dataset.quantity -= 1;
    };

    // Right block

    if (clonedBadge) clonedBadge.remove();
    if (index === -1) {
        cloned.dataset.quantity = 1;
        rightBlock.querySelector('.empty').replaceWith(cloned);
        items.push({name: nameLower, quantity: 1});
    } else {
        let rightCell = rightBlock.querySelector(`[data-name="${ name }"]`);
        let rightCellQuantity = parseInt(rightCell.dataset.quantity);
        cloned.dataset.quantity = rightCellQuantity + 1;
        cloned.insertAdjacentHTML('afterbegin', cellQuantity.replace('{{ quantity }}', rightCellQuantity + 1));
        rightCell.replaceWith(cloned);
        items[index]['quantity'] += 1;
    };

    if (operator === '+') balanceCurrent += price;
    if (operator === '-') balanceCurrent -= price;
    sellerBalance.innerText = `Your balance will be ${ balanceCurrent } UAH`;
    await handleButtons();
}

async function buy(e) {
    const item = e.currentTarget;
    const items = data['items']['buyer'];
    await handleLeftBlock(item, items, '-', blockBuy);
}

async function sell(e) {
    const item = e.currentTarget;
    const items = data['items']['seller'];
    await handleLeftBlock(item, items, '+', blockSell);
}

const cellEmpty = CELL_EMPTY;
const cellQuantity = CELL_QUANTITY;

const balanceInitial = SELLER_BALANCE_INITIAL;
const balanceGoal = SELLER_BALANCE_GOAL;

let balanceCurrent = SELLER_BALANCE_INITIAL;

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

const buyerItems = blockBuyer.querySelectorAll('[data-entity="buyer"]');
const sellerItems = blockSeller.querySelectorAll('[data-entity="seller"]');

buyerItems.forEach(item => item.addEventListener('click', buy));
sellerItems.forEach(item => item.addEventListener('click', sell));

buttonConfirm.addEventListener('click', confirmDeal);
buttonCancel.addEventListener('click', cancelDeal);
