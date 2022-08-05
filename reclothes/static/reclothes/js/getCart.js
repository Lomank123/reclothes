const cartBlock = $('#cart-header-block');

// Get cart from session cookies
function getCartData(url, callback) {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: url,
        headers: {"X-CSRFToken": csrftoken},
        method: 'GET',
        dataType: 'json',
        success: (result) => {
            console.log(result);
            callback(result);
        },
        error: (error) => {
            console.log(error);
        }
    });
}

function setCartData(data) {
    let count = 0;
    if (data.cart_items !== undefined) {
        count = Object.keys(data.cart_items).length;
    }
    const cartButton = $(`
        <a href="/cart" class="btn btn-lg" id="cart-btn">
            <i class="cart-icon bi bi-bag d-flex justify-content-center align-items-center"></i>
            ${count}
        </a>
    `);
    cartBlock.append(cartButton);
}

getCartData(cartFromSessionUrl, setCartData);
