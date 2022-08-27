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
        if ('detail' in res) {
            console.log('Error occured!');
        } else {
            cartId = parseInt(res.data.id);
            return ajaxGet(headerCartItemsUrl, data={cart_id: cartId}).then((cartItems) => {
                if ('detail' in cartItems) {
                    console.log('Error occured!');
                } else {
                    return extractProductsIds(cartItems.data);
                }
            });
        }

    });
}


ajaxGet(sessionCartUrl).then((res) => {
    if ('detail' in res) {
        console.log('Error occured!');
    } else {
        setCartData(res.data);
    }
});
