const totalPriceBlock = $('#order-total-block');
const addressBlock = $('#address-block');
const createOrderBtn = $('#create-order-btn');
const paymentFormBlock = $('#payment-form-block');

const formData = {
    address_id: null,
    payment_type: "",
};

// Address change listener
const addressSelect = $(`#address-choices`);
addressSelect.change(() => {
    let value = parseInt(addressSelect.find(':selected').val());
    if (value == NaN) {
        value = null;
    }
    formData.address_id = value;
});

// Radio buttons
const cardRadioBtn = $('#card-payment');
cardRadioBtn.click(() => {
    paymentFormBlock.show();
});

const cashRadioBtn = $('#cash-payment');
cashRadioBtn.click(() => {
    paymentFormBlock.hide();
});


function setTotalPrice(cart) {
    const totalPrice = $(`<h5 id="total-price">Total price: <b>${cart.total_price}$</b></h5>`);
    totalPriceBlock.append(totalPrice);
}


function setAddresses(addresses) {
    addresses.forEach(address => {
        const addressOption = $(`<option value=${address.id}>${address.name}</option>`);
        addressSelect.append(addressOption);
    });
}


// Order button listener
createOrderBtn.click(async () => {
    // Add card credentials
    const cardData = getCardData();
    const payment = $('input[name=payment-choice]:checked').val();

    if (payment == 'Card') {
        formData.card = cardData;
    }
    formData.payment_type = payment;
    console.log(formData);

    const result = await ajaxCall(`${defaultOrderUrl}/`, 'POST', formData);
    if ('detail' in result) {
        console.log('Error');
        return;
    }

    window.location.href = `${orderSuccessUrl}?order_id=${result.data.id}`;
});


$(window).on('load', async () => {
    // Addresses
    const addressData = await ajaxCall(addressesByCityUrl);
    if ('detail' in addressData) {
        console.log('Error occured!');
        return;
    }
    setAddresses(addressData.data.addresses);

    // Total price
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured!');
        return;
    };
    setTotalPrice(cartData.data);
});