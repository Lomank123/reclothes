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
        <button type="button" class="btn btn-lg transparent-btn" id="cart-btn">
            <i class="cart-icon bi bi-bag d-flex justify-content-center align-items-center"></i>
            ${count}
        </button>
    `);
    cartButton.click(() => {handleCartBtnClick(data.cart.id)});
    cartBlock.append(cartButton);
}

function setCartItemsData(data) {
    console.log("Cart items data set!");
}


function handleCartBtnClick(id) {
    const pageUrl = new URL(cartPageUrl);
    pageUrl.searchParams.set('cart_id', id);
    window.location.replace(`${pageUrl.href}`);
}


ajaxGet(sessionCartUrl, setCartHeaderData);
