const orderId = $('#order-id-block').data("order-id");
const filesBlock = $('#files-block');


function setFiles(products) {
    products.forEach(product => {
        const productFile = $(`
            <div class="flex-block">
                <span>Product ${product.id}</span>
            </div>
        `);
        product.files.forEach(file => {
            const downloadUrl = `${downloadFileUrl}?file_id=${file.id}&order_id=${orderId}`;
            const fileLink = $(`
                <a href="${downloadUrl}" class="btn btn-primary">
                    Download File
                </a>
            `);
            productFile.append(fileLink);
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