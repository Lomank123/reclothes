const totalPriceBlock = $(`#order-total-block`);
const addressBlock = $(`#address-block`);
const createOrderBtn = $(`#create-order-btn`);

const formData = {
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

    // Total price
    const cartData = await ajaxCall(sessionCartUrl);
    if ('detail' in cartData) {
        console.log('Error occured!');
        return;
    };
    setTotalPrice(cartData.data);
});