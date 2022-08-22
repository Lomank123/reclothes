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


function handleCartBtnClick(id) {
    const pageUrl = new URL(cartPageUrl);
    pageUrl.searchParams.set('cart_id', id);
    window.location.replace(`${pageUrl.href}`);
}


function buildCartButton(id) {
    const addToCartButton = $(`
        <button class="btn btn-primary">
            <i class="d-flex justify-content-center align-items-center bi bi-cart cart-btn"></i>
        </button>
    `);
    addToCartButton.click(() => {addToCart(id)});
    return addToCartButton;
}


function addToCart(id) {
    if (cartId !== null) {
        const data = {
            'cart': cartId,
            'product': id,
            'quantity': 1,
        }
        $.ajax({
            url: `${defaultCartItemUrl}/`,
            headers: {"X-CSRFToken": csrftoken},
            data: data,
            method: 'POST',
            dataType: 'json',
            success: (result) => {
                console.log(result);
                window.location.reload();
            },
            error: (error) => {
                console.log(error);
            }
        });
    }

}


function extractProductsIds(data) {
    const productsIds = [];
    data.cart_items.forEach(cartItem => {
        productsIds.push(cartItem.product_id);
    });
    return productsIds;
}


function getProductsIds() {
    return ajaxGet(sessionCartUrl).then((res) => {
        cartId = parseInt(res.cart.id);
        return ajaxGet(headerCartItemsUrl, data={cart_id: cartId}).then((data) => {
            return extractProductsIds(data);
        });
    });
}


ajaxGet(sessionCartUrl).then((res) => {
    setCartData(res);
});
