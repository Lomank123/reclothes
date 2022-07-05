const cartBlock = $('#cart-header-block');

// Get cart from session cookies
function getCartData() {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: `/api/cart/get_cart_from_session`,
        headers: {"X-CSRFToken": csrftoken},
        method: 'GET',
        dataType: 'json',
        success: (result) => {
            console.log(result);
            setCartData(result);
        },
        error: (error) => {
            console.log(error);
        }
    });
}

function setCartData(data) {
    const cartButton = $(`
        <a href="#" class="btn btn-lg" id="cart-btn">
            <i class="cart-icon bi bi-bag d-flex justify-content-center align-items-center"></i>
            ${data.cart.cart_items_count}
        </a>
    `);
    cartBlock.append(cartButton);
}

getCartData();
