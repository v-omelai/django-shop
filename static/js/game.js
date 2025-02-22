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
    buttonConfirm.toggleAttribute('disabled', balanceCurrent !== balanceGoal);
    buttonCancel.toggleAttribute('disabled', balanceCurrent === balanceInitial);
}

async function increaseBalance(amount) {
    balanceCurrent += parseInt(amount);
}

async function decreaseBalance(amount) {
    balanceCurrent -= parseInt(amount);
}

async function increaseQuantity(items, name) {
    const nameLower = name.toLowerCase();
    const index = items.findIndex(i => i.name === nameLower);
    if (index === -1) {
        items.push({name: nameLower, quantity: 1});
    } else {
        items[index]['quantity'] += 1
    }
}

async function decreaseQuantity(items, name) {
    const nameLower = name.toLowerCase();
    const index = items.findIndex(i => i.name === nameLower);
    if (items[index]['quantity'] === 1) {
        items.splice(index, 1);
    } else {
        items[index]['quantity'] -= 1
    }
}

async function handleFirstSide(quantity, fromItem, fromItemBadge) {
    const parsedQuantity = parseInt(quantity);
    if (parsedQuantity === 1) {
        fromItem.outerHTML = cellEmpty;
    } else if (parsedQuantity === 2) {
        fromItemBadge.remove();
        fromItem.dataset.quantity = 1;
    } else {
        fromItemBadge.innerText = parsedQuantity - 1;
        fromItem.dataset.quantity -= 1;
    };
}

async function handleSecondSide(items, name, toItem, toItemBadge, toBlock) {
    const toCell = toBlock.querySelector(`[data-name="${ name }"]`);
    if (toItemBadge) toItemBadge.remove();
    if (toCell) {
        const toCellQuantity = parseInt(toCell.dataset.quantity);
        toItem.dataset.quantity = toCellQuantity + 1;
        toItem.insertAdjacentHTML('afterbegin', cellQuantity.replace('{{ quantity }}', toCellQuantity + 1));
        toCell.replaceWith(toItem);
    } else {
        toItem.dataset.quantity = 1;
        toBlock.querySelector('.empty').replaceWith(toItem);
    }
}

async function handleItems(fromItem, items, funcBalance, funcQuantity, fromBlock, toBlock) {
    let toItem = fromItem.cloneNode(true);

    const toItemBadge = toItem.querySelector('.quantity');
    const fromItemBadge = fromItem.querySelector('.quantity');

    const name = fromItem.dataset.name;
    const price = fromItem.dataset.price;
    const quantity = fromItem.dataset.quantity;

    await handleFirstSide(quantity, fromItem, fromItemBadge);
    await handleSecondSide(items, name, toItem, toItemBadge, toBlock);

    toItem.addEventListener('click', async (e) => {
        let b = funcBalance === increaseBalance ? decreaseBalance : increaseBalance
        let q = funcQuantity === increaseQuantity ? decreaseQuantity : increaseQuantity
        await handleItems(toItem, items, b, q, toBlock, fromBlock)
    });

    await funcQuantity(items, name);
    await funcBalance(price);
    await handleButtons();

    sellerBalance.innerText = `Your balance will be ${ balanceCurrent } UAH`;
}

async function buy(e) {
    await handleItems(
        e.currentTarget, data.items.buyer,
        decreaseBalance, increaseQuantity,
        blockBuyer, blockBuy,
    );
}

async function sell(e) {
    await handleItems(
        e.currentTarget, data.items.seller,
        increaseBalance, increaseQuantity,
        blockSeller, blockSell,
    );
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
