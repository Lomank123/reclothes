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
        const newItem = $(`<div class="default-block single-cart-item"></div>`);
        const infoBlock = $(`
            <div class="item-info-block">
                <a href="/product/${item.product_id}">${item.product_title}</a>
            </div>
        `);
        const quantityBlock = buildQuantityBlock(item.quantity, item.id, item.product_id);
        const deleteItemButton = $(`
            <button type="button" class="btn btn-primary delete-cart-item-btn">
                <i class="bi bi-trash d-flex justify-content-center align-items-center"></i>
            </button>
        `);
        deleteItemButton.click(() => {deleteCartItem(item.id)});

        newItem.append(infoBlock);
        newItem.append(quantityBlock);
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

    addBtn.click(() => {changeQuantity(currentQuantity + 1, id, productId)});
    subBtn.click(() => {changeQuantity(currentQuantity - 1, id, productId)});

    quantityBlock.append(addBtn);
    quantityBlock.append(quantityField);
    quantityBlock.append(subBtn);
    return quantityBlock;
}


function changeQuantity(newQuantity, id, productId) {
    const data = {
        value: newQuantity,
        cart_item_id: id,
        product_id: productId,
    }
    $.ajax({
        url: `${changeCartItemQuantityUrl}/`,
        headers: {"X-CSRFToken": csrftoken},
        data: data,
        method: 'POST',
        dataType: 'json',
        success: () => {
            window.location.reload();
        },
        error: (error) => {
            console.log(error.responseText);
        }
    });
}


function deleteCartItem(id) {
    $.ajax({
        url: `${defaultCartItemUrl}/${id}`,
        headers: {"X-CSRFToken": csrftoken},
        method: 'DELETE',
        dataType: 'json',
        success: () => {
            window.location.reload();
        },
        error: (error) => {
            console.log(error.responseText);
        },
    });
}


function setCartItemsData(data) {
    setPaginatedCartItems(data.cart_items.results);
    setPagination(data.cart_items);
}


ajaxGet(paginatedCartItemsUrl, setCartItemsData);
