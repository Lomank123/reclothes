const totalPriceBlock = $('#order-total-block');
const createOrderBtn = $('#create-order-btn');

const formData = {};


function setTotalPrice(cart) {
    const totalPrice = $(`<h5 id="total-price">Total price: <b>${cart.total_price}$</b></h5>`);
    totalPriceBlock.append(totalPrice);
}


// Order button listener
createOrderBtn.click(async () => {
    // Add card credentials
    const cardData = getCardData();
    formData.card = cardData;
    console.log(formData);

    const result = await ajaxCall(`${defaultOrderUrl}/`, 'POST', formData);
    if ('detail' in result) {
        console.log('Error');
        return;
    }

    window.location.href = `${orderUrl}/${result.data.id}/`;
});


$(window).on('load', async () => {
    // Total price
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured!');
        return;
    };
    setTotalPrice(cartData.data);
});