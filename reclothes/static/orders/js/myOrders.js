const mainBlock = $('#my-orders-main-block');


function setMyOrders(orders) {
    orders.forEach(order => {
        const orderBlock = $(`<div class="order-block default-block"></div>`);

        // Order main info
        const orderInfoBlock = $(`
            <div class="order-info-block flex-block">
                <span>ID: ${order.id}</span>
                <span>Created: ${order.created_at}</span>
                <span>Last update: ${order.updated_at}</span>
                <span>Status: ${order.status}</span>
                <span>Total price: ${order.total_price}</span>
            </div>
        `);

        // Order items
        const itemsBlock = $(`<div class="items-block flex-block"></div>`);
        order.order_items.forEach(item => {
            const itemBlock = $(`
                <div class="item-block flex-block">
                    <span>Order item ID: ${item.id}</span>
                </div>
            `);
            itemsBlock.append(itemBlock);
        });

        orderBlock.append(orderInfoBlock);
        orderBlock.append($(`<hr />`));
        orderBlock.append(itemsBlock);
        orderBlock.append($(`<hr />`));
        mainBlock.append(orderBlock);
    });
}


$(window).on('load', async () => {
    const orders = await ajaxCall(defaultOrderUrl);
    if ('detail' in orders) {
        console.log('Error occured!');
        return;
    };
    setMyOrders(orders);
});