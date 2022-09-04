const totalPriceBlock = $(`#order-total-block`);
const addressBlock = $(`#address-block`);
const createOrderBtn = $(`#create-order-btn`);

const formData = {
    cart_id: null,
    total_price: null,
    address_id: null,
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


function setTotalPrice(cart) {
    const totalPrice = $(`<span id="total-price">Total price: <b>${cart.total_price}$</b></span>`);
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
    console.log(formData);
    const result = await ajaxCall(`${defaultOrderUrl}/`, 'POST', formData);
    if ('detail' in result) {
        console.log('Error');
        return;
    }
});


$(window).on('load', async () => {
    // Addresses
    const addressData = await ajaxCall(addressesByCityUrl);
    if ('detail' in addressData) {
        console.log('Error occured!');
        return;
    }
    setAddresses(addressData.data.addresses);

    // Total price and cart data
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured!');
        return;
    };
    // Set cart data to form
    formData.total_price = cartData.data.total_price;
    formData.cart_id = cartData.data.id;
    // Display total price
    setTotalPrice(cartData.data);

});