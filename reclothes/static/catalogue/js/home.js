function displayHomeData(result) {
    setBestProducts(result.best_products);
    setHotProducts(result.hot_products);
    setNewestProducts(result.newest_products);
}

function setBestProducts(data) {
    const bestProductsBlock = $("#best-products-block");
    bestProductsBlock.empty();
    data.forEach((product) => {
        const info = $(`
            <div class="flex-block">
                <a href="/product/${product.id}">Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
                <span>Rating: ${product.avg_rate}</span>
            </div>
        `);
        bestProductsBlock.append(info);
    });
}

function setHotProducts(data) {
    const hotProductsBlock = $("#hot-products-block");
    hotProductsBlock.empty();
    data.forEach((product) => {
        const info = $(`
            <div class="flex-block">
                <a href="/product/${product.id}">Title: ${product.title}</a>
                <span>Type: ${product.type}</span>
                <span>Price: ${product.regular_price}</span>
                <span>Purchases: ${product.purchases}</span>
            </div>
        `);
        hotProductsBlock.append(info);
    });
}

function setNewestProducts(data) {
    const newestProductsBlock = $("#newest-products-block");
    newestProductsBlock.empty();
    data.forEach((product) => {
        const info = $(`
            <div class="flex-block">
            <a href="/product/${product.id}">Title: ${product.title}</a>
            <span>Type: ${product.type}</span>
            <span>Price: ${product.regular_price}</span>
            </div>
        `);
        newestProductsBlock.append(info);
    });
}

ajaxGet(homeProductsUrl, displayHomeData);
