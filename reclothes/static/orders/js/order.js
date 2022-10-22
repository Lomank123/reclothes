const totalPriceBlock = $('#order-total-block');
const paymentForm = $('#payment-form');

const formData = {};


function setTotalPrice(cart) {
    const totalPrice = $(`<h5 id="total-price">Total price: <b>${cart.total_price}$</b></h5>`);
    totalPriceBlock.append(totalPrice);
}


async function checkCard() {
    const cardData = getCardData();
    try {
        return await ajaxCall(`${defaultCardUrl}/`, 'POST', cardData);
    } catch(err) {
        setErrors(err.responseJSON);
        return err.responseJSON;
    }
}


paymentForm.submit(async (e) => {
    e.preventDefault();

    const cardResponse = await checkCard();
    // If card credentials were valid
    if (cardResponse.detail) {
        const result = await ajaxCall(`${defaultOrderUrl}/`, 'POST', formData);
        window.location.href = `${orderUrl}/${result.id}/`;
    }
});


$(window).on('load', async () => {
    // Total price
    const cartData = await ajaxCall(currentCartUrl);
    setTotalPrice(cartData);
});