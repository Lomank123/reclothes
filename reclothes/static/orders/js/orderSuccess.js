const orderId = $('#order-id-block').data("order-id");
const filesBlock = $('#files-block');


function setFiles(products) {
    products.forEach(product => {
        const productFile = $(`
            <div class="flex-block">
                <span class="product-label"><b>Product ${product.id}</b></span>
            </div>
        `);
        product.keys.forEach(key => {
            const keyBlock = $(`
                <div class="flex-block">
                    <span><b>Activation key</b></span>
                    <span><b>Key:</b> ${key.key}</span>
                </div>
            `);
            productFile.append(keyBlock);
        });
        product.files.forEach(file => {
            const downloadUrl = `${downloadFileUrl}?file_id=${file.id}&order_id=${orderId}`;
            const fileBlock = $(`
                <div class="flex-block file-block">
                    <div class="flex-block">
                        <span><b>File</b></span>
                        <span><b>Name:</b> ${file.name}</span>
                        <span><b>Size:</b> ${file.size}</span>
                        <span><b>Alt link:</b> ${file.link}</span>
                    </div>
                </div>
            `);
            const fileLink = $(`<a href="${downloadUrl}" class="btn btn-primary download-btn">Download File</a>`);
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