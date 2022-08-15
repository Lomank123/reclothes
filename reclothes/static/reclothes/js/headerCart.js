const cartBlock = $('#cart-header-block');

function setCartHeaderData(data) {
    setCartData(data);
    ajaxGet(headerCartItemsUrl, setCartItemsData, data={cart_id: data.cart.id});
}

function calculateItemsCount(count) {
    let countString = count.toString();
    if (count > 10) {
        countString += '+';
    }
    return countString;
}

function setCartData(data) {
    const count = calculateItemsCount(data.cart.items_count);
    const cartButton = $(`
        <a href="/cart" class="btn btn-lg" id="cart-btn">
            <i class="cart-icon bi bi-bag d-flex justify-content-center align-items-center"></i>
            ${count}
        </a>
    `);
    cartBlock.append(cartButton);
}

function setCartItemsData(data) {
    console.log("Cart items data set!");
}

ajaxGet(sessionCartUrl, setCartHeaderData);
