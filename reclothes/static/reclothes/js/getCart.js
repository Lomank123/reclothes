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
        },
        error: (error) => {
            console.log(error);
        }
    });
}

getCartData();
