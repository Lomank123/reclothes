const cartBlock = $('#cart-header-block');
let cartId = null;


function calculateItemsCount(count) {
    let countString = count.toString();
    if (count > 10) {
        countString += '+';
    }
    return countString;
}

function setCartData(cart) {
    const count = calculateItemsCount(cart.items_count);
    const cartButton = $(`
        <a href="${cartPageUrl}/" class="btn btn-lg transparent-btn" id="cart-btn">
            <i class="cart-icon bi bi-bag d-flex justify-content-center align-items-center"></i>
            ${count}
        </a>
    `);
    cartBlock.append(cartButton);
}


function buildCartButton(id) {
    const addToCartButton = $(`
        <button class="btn btn-primary">
            <i class="d-flex justify-content-center align-items-center bi bi-cart cart-btn"></i>
        </button>
    `);
    addToCartButton.click(async () => {await addToCart(id)});
    return addToCartButton;
}


async function addToCart(id) {
    if (cartId === null) {
        console.log('Cart id is null, cannot add to cart.');
        return;
    }

    const data = {
        'cart': cartId,
        'product': id,
        'quantity': 1,
    }
    const result = await ajaxCall(`${defaultCartItemUrl}/`, 'POST', data);
    window.location.reload();
}


async function getProductsIds() {
    const cartData = await ajaxCall(currentCartUrl);
    const url = `${cartItemUrl}/?cart=${cartData.id}`;
    const cartItemsData = await ajaxCall(url);
    cartId = parseInt(cartData.id);
    const productsIds = [];
    cartItemsData.forEach(cartItem => {
        productsIds.push(cartItem.product_id);
    });
    return productsIds;
}


$(window).on('load', async () => {
    const cartData = await ajaxCall(currentCartUrl);
    setCartData(cartData);
});
