const mainBlock = $('#my-orders-block');


function setMyOrders(orders) {
    orders.forEach(order => {
        const orderBlock = $(`<div class="order-block default-block"></div>`);

        // Order main info
        const orderInfoBlock = $(`
            <div class="order-info-block flex-block">
                <span><b><a href="${orderUrl}/${order.id}/">Order ${order.id}</a></b></span>
                <span>Status: ${order.status}</span>
                <span>Total price: ${order.total_price}</span>

                <span>Created: ${order.created_at}</span>
                <span>Last update: ${order.updated_at}</span>
            </div>
        `);

        orderBlock.append(orderInfoBlock);
        mainBlock.append(orderBlock);
    });
}


$(window).on('load', async () => {
    const orders = await ajaxCall(myOrdersUrl);
    if ('detail' in orders) {
        console.log('Error occured!');
        return;
    };
    setMyOrders(orders.results);
    setPagination(orders);
});