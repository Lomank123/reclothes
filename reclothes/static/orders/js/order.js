const totalPriceBlock = $('#order-total-block');
const paymentForm = $('#payment-form');

const formData = {};


function setTotalPrice(cart) {
    const totalPrice = $(`<h5 id="total-price">Total price: <b>${cart.total_price}$</b></h5>`);
    totalPriceBlock.append(totalPrice);
}


paymentForm.submit(async (e) => {
    e.preventDefault();

    // Add card credentials
    const cardData = getCardData();
    formData.card = cardData;
    console.log(formData);

    try {
        const result = await ajaxCall(`${defaultOrderUrl}/`, 'POST', formData);
        window.location.href = `${orderUrl}/${result.data.id}/`;
    } catch(err) {
        setErrors(err.responseJSON.detail.card);
    }
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