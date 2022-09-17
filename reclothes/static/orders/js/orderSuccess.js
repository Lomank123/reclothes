$(window).on('load', async () => {
    const orderId = $('#order-id-block').data("order-id");
    const url = `${downloadProductFileUrl}?order_id=${orderId}`;
    const fileData = await ajaxCall(url);

    if ('detail' in fileData) {
        console.log('Error occured!');
        return;
    };
});