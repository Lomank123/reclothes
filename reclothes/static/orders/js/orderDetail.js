const filesBlock = $('#files-block');
const orderBlock = $('#order-detail-info-block');
const orderId = filesBlock.data("order-id");


function setFiles(products) {
    products.forEach(product => {
        const productFile = $(`
            <div class="default-block">
                <span class="product-label">
                    <b><a href="${productDetailUrl}/${product.id}/">${product.title}</b></a>
                </span>
                <div class="flex-block">
                    <span><b>Guide</b></span>
                    <span>${product.guide}</span>
                </div>
            </div>
        `);

        if (product.keys.length > 0) {
            productFile.append($(`<hr />`));
            productFile.append($(`<span><b>Activation keys</b></span>`));
        }

        product.keys.forEach(key => {
            const keyBlock = $(`
                <div class="flex-block">
                    <span>${key.key}</span>
                </div>
            `);
            productFile.append(keyBlock);
        });

        if (product.files.length > 0) {
            productFile.append($(`<hr />`));
            productFile.append($(`<span><b>Files</b></span>`));
        }

        product.files.forEach(file => {
            const fileBlock = $(`<div class="flex-block"></div>`);
            const fileLink = $(`<a href="${downloadFileUrl}/${file.token}/">${file.name} (${file.size}KB)</a>`);
            fileBlock.append(fileLink);
            productFile.append(fileBlock);
        });
        filesBlock.append(productFile);
    });
}


function setOrderInfo(order) {
    // Order main info
    const infoBlock = $(`
        <div class="order-info-block flex-block">
            <span><b><a href="${orderUrl}/${order.id}/">Order ${order.id}</a></b></span>
            <span>Status: ${order.status}</span>
            <span>Total price: ${order.total_price}</span>

            <span>Created: ${order.created_at}</span>
            <span>Last update: ${order.updated_at}</span>
        </div>
    `);
    orderBlock.append(infoBlock);
}


$(window).on('load', async () => {
    const url = `${orderFileUrl}/${orderId}/`;
    const orderData = await ajaxCall(url);
    setFiles(orderData.detail.products);
    setOrderInfo(orderData.detail.order);
});
