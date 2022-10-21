function displayHomeData(result, productsIds) {
    setBestProducts(result.best_products, productsIds);
    setHotProducts(result.hot_products, productsIds);
    setNewestProducts(result.newest_products, productsIds);
}

function setBestProducts(data, ids) {
    const bestProductsBlock = $('#best-products-block');
    bestProductsBlock.empty();
    data.forEach((product) => {
        const singleProductBlock = $(`<div class='single-product-block'></div>`);
        const info = $(`
            <div class='flex-block'>
                <a href='/product/${product.id}'>Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
                <span>Rating: ${product.avg_rate}</span>
            </div>
        `);
        const cartBtn = buildCartButton(product.id);
        if (ids.includes(product.id)) {
            cartBtn.prop('disabled', true);
        }
        singleProductBlock.append(info);
        singleProductBlock.append(cartBtn);
        bestProductsBlock.append(singleProductBlock);
    });
}


function setHotProducts(data, ids) {
    const hotProductsBlock = $('#hot-products-block');
    hotProductsBlock.empty();
    data.forEach((product) => {
        const singleProductBlock = $(`<div class='single-product-block'></div>`);
        const info = $(`
            <div class='flex-block'>
                <a href='/product/${product.id}'>Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
                <span>Purchases: ${product.purchases}</span>
            </div>
        `);
        const cartBtn = buildCartButton(product.id);
        if (ids.includes(parseInt(product.id))) {
            cartBtn.prop('disabled', true);
        }
        singleProductBlock.append(info);
        singleProductBlock.append(cartBtn);
        hotProductsBlock.append(singleProductBlock);
    });
}

function setNewestProducts(data, ids) {
    const newestProductsBlock = $('#newest-products-block');
    newestProductsBlock.empty();
    data.forEach((product) => {
        const singleProductBlock = $(`<div class='single-product-block'></div>`);
        const info = $(`
            <div class='flex-block'>
                <a href='/product/${product.id}'>Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
            </div>
        `);
        const cartBtn = buildCartButton(product.id);
        if (ids.includes(parseInt(product.id))) {
            cartBtn.prop('disabled', true);
        }
        singleProductBlock.append(info);
        singleProductBlock.append(cartBtn);
        newestProductsBlock.append(singleProductBlock);
    });
}


$(window).on('load', async () => {
    const productsIds = await getProductsIds();
    const homeData = await ajaxCall(homeProductsUrl);
    displayHomeData(homeData, productsIds);
});
