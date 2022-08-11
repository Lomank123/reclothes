const cartBlock = $('#cart-header-block');

// Get cart from session cookies
function ajaxGet(url, callback) {
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

function setCartHeaderData(data) {
    setCartData(data);
    setCartItemsData(data);
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

ajaxGet(headerCartUrl, setCartHeaderData);
