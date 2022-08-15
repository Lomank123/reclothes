function setPaginatedCartItems(data) {
    console.log("Paginated cart items done!");
}

function getPaginatedCartItems(data) {
    ajaxGet(paginatedCartItemsUrl, setPaginatedCartItems, data={cart_id: data.cart.id});
}

ajaxGet(sessionCartUrl, getPaginatedCartItems)