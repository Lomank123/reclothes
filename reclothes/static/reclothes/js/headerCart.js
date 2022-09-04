const cartBlock = $('#cart-header-block');
let cartId = null;


function calculateItemsCount(count) {
    let countString = count.toString();
    if (count > 10) {
        countString += '+';
    }
    return countString;
}

function setCartData(data) {
    const count = calculateItemsCount(data.items_count);
    const cartButton = $(`
        <button type="button" class="btn btn-lg transparent-btn" id="cart-btn">
            <i class="cart-icon bi bi-bag d-flex justify-content-center align-items-center"></i>
            ${count}
        </button>
    `);
    cartButton.click(() => {handleCartBtnClick(data.id)});
    cartBlock.append(cartButton);
}


function handleCartBtnClick(id) {
    const pageUrl = new URL(cartPageUrl);
    pageUrl.searchParams.set('cart_id', id);
    window.location.replace(pageUrl.href);
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
    if ('detail' in result) {
        console.log(result);
        return;
    }
    window.location.reload();
}


async function getProductsIds() {
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured with cart.');
        return;
    }

    cartId = parseInt(cartData.data.id);
    cartItemsData = await ajaxCall(headerCartItemsUrl, 'GET', {cart_id: cartId});
    if ('detail' in cartItemsData) {
        console.log('Error occured with cart items.');
        return;
    }

    const productsIds = [];
    cartItemsData.data.cart_items.forEach(cartItem => {
        productsIds.push(cartItem.product_id);
    });
    return productsIds;
}


$(window).on('load', async () => {
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured with cart');
        return;
    }
    setCartData(cartData.data);
});
