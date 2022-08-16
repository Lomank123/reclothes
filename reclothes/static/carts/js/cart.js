const cartItemsBlock = $('#cart-items-block');
const orderBtn = $('#order-create-btn');
const paginationBlock = $('#pagination-block');


function setPaginatedCartItems(cartItems) {
    if (cartItems.length == 0) {
        const emptyMsg = $(`<span>Cart is empty.</span>`);
        cartItemsBlock.append(emptyMsg);
        orderBtn.hide();
        return;
    }
    cartItems.forEach(item => {
        const newItem = $(`
            <div class="default-block single-cart-item">
                <span>${item.product_title}</span>
                <span>${item.quantity}</span>
            </div>
        `);
        cartItemsBlock.append(newItem);
    });
}


function setCartItemsData(data) {
    setPaginatedCartItems(data.cart_items.results);
    setPagination(data.cart_items);
}


ajaxGet(paginatedCartItemsUrl, setCartItemsData);
