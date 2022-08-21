let productsIds = [];


function displayHomeData(result) {
    setBestProducts(result.best_products);
    setHotProducts(result.hot_products);
    setNewestProducts(result.newest_products);
}

function setBestProducts(data) {
    const bestProductsBlock = $("#best-products-block");
    bestProductsBlock.empty();
    data.forEach((product) => {
        const singleProductBlock = $(`<div class="single-product-block"></div>`);
        const info = $(`
            <div class="flex-block">
                <a href="/product/${product.id}">Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
                <span>Rating: ${product.avg_rate}</span>
            </div>
        `);
        const cartBtn = buildCartButton(product.id);
        if (productsIds.includes(product.id)) {
            cartBtn.prop('disabled', true);
        }
        singleProductBlock.append(info);
        singleProductBlock.append(cartBtn);
        bestProductsBlock.append(singleProductBlock);
    });
}


function setHotProducts(data) {
    const hotProductsBlock = $("#hot-products-block");
    hotProductsBlock.empty();
    data.forEach((product) => {
        const singleProductBlock = $(`<div class="single-product-block"></div>`);
        const info = $(`
            <div class="flex-block">
                <a href="/product/${product.id}">Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
                <span>Purchases: ${product.purchases}</span>
            </div>
        `);
        const cartBtn = buildCartButton(product.id);
        if (productsIds.includes(parseInt(product.id))) {
            cartBtn.prop('disabled', true);
        }
        singleProductBlock.append(info);
        singleProductBlock.append(cartBtn);
        hotProductsBlock.append(singleProductBlock);
    });
}

function setNewestProducts(data) {
    const newestProductsBlock = $("#newest-products-block");
    newestProductsBlock.empty();
    data.forEach((product) => {
        const singleProductBlock = $(`<div class="single-product-block"></div>`);
        const info = $(`
            <div class="flex-block">
            <a href="/product/${product.id}">Title: ${product.title}</a>
            <span>Type: ${product.type}</span>
            <span>Price: ${product.regular_price}</span>
            </div>
        `);
        const cartBtn = buildCartButton(product.id);
        if (productsIds.includes(parseInt(product.id))) {
            cartBtn.prop('disabled', true);
        }
        singleProductBlock.append(info);
        singleProductBlock.append(cartBtn);
        newestProductsBlock.append(singleProductBlock);
    });
}


function getProductsIds(data) {
    cartId = parseInt(data.cart.id);
    ajaxGet(headerCartItemsUrl, setProductsIds, data={cart_id: cartId});
}


function setProductsIds(data) {
    data.cart_items.forEach(cartItem => {
        productsIds.push(cartItem.product_id);
    });
    ajaxGet(homeProductsUrl, displayHomeData);
}

ajaxGet(sessionCartUrl, getProductsIds);
