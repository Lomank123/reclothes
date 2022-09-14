
$(window).on('load', async () => {
    const orders = await ajaxCall(defaultOrderUrl);
    if ('detail' in orders) {
        console.log('Error occured!');
        return;
    };
});