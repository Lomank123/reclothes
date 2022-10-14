const cartItemsBlock = $('#cart-items-block');
const orderBtn = $('#order-create-btn');
const paginationBlock = $('#pagination-block');
const totalPriceBlock = $('#cart-total-price-block');


function setPaginatedCartItems(cartItems) {
    if (cartItems.length == 0) {
        const emptyMsg = $(`<span>Cart is empty.</span>`);
        cartItemsBlock.append(emptyMsg);
        orderBtn.hide();
        return;
    }
    cartItems.forEach(item => {
        const newItem = $(`<div class="default-block single-cart-item"></div>`);
        const infoBlock = $(`
            <div class="item-info-block">
                <a href="/product/${item.product_id}">${item.product_title}</a>
                <span class="item-total-price">Price: ${item.total_price}$</span>
            </div>
        `);

        newItem.append(infoBlock);
        if (item.product_is_limited > 0) {
            const quantityBlock = buildQuantityBlock(item.quantity, item.id, item.product_id);
            newItem.append(quantityBlock);
        }
        cartItemsBlock.append(newItem);
    });
}


function buildQuantityBlock(quantity, id, productId) {
    const addBtn = $(`<button type="button" class="btn btn-primary quantity-btn">+</button>`);
    const subBtn = $(`<button type="button" class="btn btn-primary quantity-btn">-</button>`);
    const quantityField = $(`<span class="quantity-field">${quantity}</span>`);
    const quantityInfoBlock = $(`<div class="quantity-info-block"></div>`);
    const quantityBlock = $(`<div class="quantity-block"></div>`);
    const errorBlock = $(`<div class="quantity-error-block"></div>`);
    const currentQuantity = parseInt(quantity);

    const deleteItemButton = $(`
        <button type="button" class="btn btn-primary delete-cart-item-btn">
            <i class="bi bi-trash d-flex justify-content-center align-items-center"></i>
        </button>
    `);

    deleteItemButton.click(async () => {await deleteCartItem(item.id)});
    addBtn.click(async () => {await changeQuantity(currentQuantity + 1, id, productId, errorBlock)});
    subBtn.click(async () => {await changeQuantity(currentQuantity - 1, id, productId, errorBlock)});

    quantityInfoBlock.append(addBtn);
    quantityInfoBlock.append(quantityField);
    quantityInfoBlock.append(subBtn);
    quantityInfoBlock.append(deleteItemButton);
    quantityBlock.append(quantityInfoBlock);
    quantityBlock.append(errorBlock);
    return quantityBlock;
}


async function changeQuantity(newQuantity, id, productId, block) {
    const data = {
        value: newQuantity,
        cart_item_id: id,
        product_id: productId,
    };
    const url = `${changeCartItemQuantityUrl}/`;
    try {
        const result = await ajaxCall(url, 'PATCH', data);
        window.location.reload();
    } catch(err) {
        setQuantityErrors(err.responseJSON, block);
    }
}


function setQuantityErrors(error, block) {
    block.empty();
    const errorMessageBlock = $(`
        <div class="error-msg-block flex-block">
            <span>${error.detail}</span>
        </div>
    `);
    block.append(errorMessageBlock);
}


async function deleteCartItem(id) {
    const url = `${defaultCartItemUrl}/${id}/`;
    await ajaxCall(url, 'DELETE');
    window.location.reload();
}


function setCartItemsData(data) {
    setPaginatedCartItems(data.cart_items.results);
    setPagination(data.cart_items);
}


function setTotalPrice(totalPrice) {
    if (totalPrice === null) {
        totalPriceBlock.hide();
        return;
    }

    const priceBlock = $(`
        <div id="total-price">
            <span>Total price: ${totalPrice}$</span>
        </div>
    `);
    totalPriceBlock.append(priceBlock);
}


$(window).on('load', async () => {
    // Here we need to get paginated cart items as well
    const cartData = await ajaxCall(`${currentCartUrl}/?items=true&paginate=true`);
    setTotalPrice(cartData.detail.cart.total_price);
    setCartItemsData(cartData.detail);
});
