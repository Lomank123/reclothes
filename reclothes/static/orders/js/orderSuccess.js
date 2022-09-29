const orderId = $('#order-id-block').data("order-id");
const filesBlock = $('#files-block');


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
            const downloadUrl = `${downloadFileUrl}?file_id=${file.id}&order_id=${orderId}`;
            const fileBlock = $(`<div class="flex-block"></div>`);
            const fileLink = $(`<a href="${downloadUrl}">${file.name} (${file.size}KB)</a>`);
            fileBlock.append(fileLink);
            productFile.append(fileBlock);
        });
        filesBlock.append(productFile);
    });
}



$(window).on('load', async () => {
    const url = `${orderFileUrl}?order_id=${orderId}`;
    const fileData = await ajaxCall(url);

    if ('detail' in fileData) {
        console.log('Error occured!');
        return;
    };

    setFiles(fileData.data.products);
});