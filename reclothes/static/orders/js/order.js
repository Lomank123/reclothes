function setAddresses(addresses) {
    console.log(addresses);
}


$(window).on('load', async () => {
    const addressData = await ajaxGet(addressesByCityUrl);
    if ('detail' in addressData) {
        console.log('Error occured!');
    } else {
        setAddresses(addressData.data);
    };
});