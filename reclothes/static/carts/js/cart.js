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
        const quantityBlock = buildQuantityBlock(
            item.quantity,
            item.id,
            item.product_id,
            item.product_is_limited,
        );
        newItem.append(quantityBlock);
        cartItemsBlock.append(newItem);
    });
}


function buildQuantityBlock(quantity, id, productId, is_limited) {
    const addBtn = $(`<button type="button" class="btn btn-primary quantity-btn">+</button>`);
    const subBtn = $(`<button type="button" class="btn btn-primary quantity-btn">-</button>`);
    const quantityField = $(`<span class="quantity-field">${quantity}</span>`);
    const quantityInfoBlock = $(`<div class="quantity-info-block"></div>`);
    const quantityInfoBlock1 = $(`<div class="quantity-info-block"></div>`);
    const quantityBlock = $(`<div class="quantity-block"></div>`);
    const errorBlock = $(`<div class="quantity-error-block"></div>`);
    const currentQuantity = parseInt(quantity);

    const deleteItemButton = $(`
        <button type="button" class="btn btn-primary delete-cart-item-btn">
            <i class="bi bi-trash d-flex justify-content-center align-items-center"></i>
        </button>
    `);

    deleteItemButton.click(async () => {await deleteCartItem(id)});
    addBtn.click(async () => {await changeQuantity(currentQuantity + 1, id, errorBlock)});
    subBtn.click(async () => {await changeQuantity(currentQuantity - 1, id, errorBlock)});

    quantityInfoBlock.append(addBtn);
    quantityInfoBlock.append(quantityField);
    quantityInfoBlock.append(subBtn);
    quantityInfoBlock1.append(quantityInfoBlock);
    quantityInfoBlock1.append(deleteItemButton);
    quantityBlock.append(quantityInfoBlock1);

    if (is_limited === 0) {
        quantityInfoBlock.hide();
    }

    quantityBlock.append(errorBlock);
    return quantityBlock;
}


async function changeQuantity(newQuantity, id, block) {
    const data = {quantity: newQuantity};
    const url = `${cartItemUrl}/${id}/`;
    try {
        await ajaxCall(url, 'PATCH', data);
        window.location.reload();
    } catch(err) {
        setQuantityErrors(err.responseJSON, block);
    }
}


function setQuantityErrors(error, block) {
    block.empty();
    const errorMessageBlock = $(`
        <div class="error-msg-block flex-block">
            <span>${error.quantity}</span>
        </div>
    `);
    block.append(errorMessageBlock);
}


async function deleteCartItem(id) {
    const url = `${defaultCartItemUrl}/${id}/`;
    await ajaxCall(url, 'DELETE');
    window.location.reload();
}


function setCartItemsData(cartItems) {
    setPaginatedCartItems(cartItems.results);
    setPagination(cartItems);
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
    const cartData = await ajaxCall(currentCartUrl);
    const url = `${cartItemUrl}/?cart=${cartData.id}&paginate=true`;
    const cartItemsData = await ajaxCall(url);
    setTotalPrice(cartData.total_price);
    setCartItemsData(cartItemsData);
});
