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
        const deleteItemButton = $(`
            <button type="button" class="btn btn-primary delete-cart-item-btn">
                <i class="bi bi-trash d-flex justify-content-center align-items-center"></i>
            </button>
        `);
        deleteItemButton.click(async () => {await deleteCartItem(item.id)});

        newItem.append(infoBlock);
        if (item.product_is_limited > 0) {
            const quantityBlock = buildQuantityBlock(item.quantity, item.id, item.product_id);
            newItem.append(quantityBlock);
        }
        newItem.append(deleteItemButton);
        cartItemsBlock.append(newItem);
    });
}


function buildQuantityBlock(quantity, id, productId) {
    const addBtn = $(`<button type="button" class="btn btn-primary quantity-btn">+</button>`);
    const subBtn = $(`<button type="button" class="btn btn-primary quantity-btn">-</button>`);
    const quantityField = $(`<span class="quantity-field">${quantity}</span>`);
    const quantityBlock = $(`<div class="quantity-block"></div>`);
    const currentQuantity = parseInt(quantity);

    addBtn.click(async () => {await changeQuantity(currentQuantity + 1, id, productId)});
    subBtn.click(async () => {await changeQuantity(currentQuantity - 1, id, productId)});

    quantityBlock.append(addBtn);
    quantityBlock.append(quantityField);
    quantityBlock.append(subBtn);
    return quantityBlock;
}


async function changeQuantity(newQuantity, id, productId) {
    const data = {
        value: newQuantity,
        cart_item_id: id,
        product_id: productId,
    };
    const url = `${changeCartItemQuantityUrl}/`;
    const result = await ajaxCall(url, 'PATCH', data);
    window.location.reload();
}


async function deleteCartItem(id) {
    const url = `${defaultCartItemUrl}/${id}`;
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
    // Cart
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured!');
        return;
    }
    setTotalPrice(cartData.data.total_price);

    // Cart Items
    const paginatedData = await ajaxCall(paginatedCartItemsUrl);
    if ('detail' in paginatedData) {
        console.log('Error occured!');
        return;
    }
    setCartItemsData(paginatedData.data);
});
