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
    // Nested dicts should be converted to json
    formData.card = JSON.stringify(cardData);

    try {
        const result = await ajaxCall(`${defaultOrderUrl}/`, 'POST', formData);
        window.location.href = `${orderUrl}/${result.detail.id}/`;
    } catch(err) {
        setErrors(err.responseJSON);
    }
});


$(window).on('load', async () => {
    // Total price
    const cartData = await ajaxCall(currentCartUrl);
    setTotalPrice(cartData.detail.cart);
});