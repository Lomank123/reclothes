function getCardData() {
    const cardExpiryYear = $('#card-year').val();
    const cardExpiryMonth = $('#card-month').val();
    const cardHolderName = $('#card-holder').val();
    const cardNum = $('#card-number').val();
    const cardCode = $('#card-code').val();

    const cardData = {
        name: cardHolderName,
        number: cardNum,
        code: cardCode,
        expiry_date: `${cardExpiryMonth}/${cardExpiryYear}`,
    };
    return cardData;
}