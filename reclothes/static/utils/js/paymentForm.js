const fields = {
    'code': {
        'block': $('#card-code-error-block'),
        'inputs': [$('#card-code')],
    },
    'expiry_date': {
        'block': $('#card-expiry-date-error-block'),
        'inputs': [$('#card-year'), $('#card-month')],
    },
    'number': {
        'block': $('#card-number-error-block'),
        'inputs': [$('#card-number')],
    },
    'name': {
        'block': $('#card-holder-error-block'),
        'inputs': [$('#card-holder')],
    },
}


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


function setErrors(errors) {
    // Clear errors
    for (const [key, value] of Object.entries(fields)) {
        value.block.empty();
        value.inputs.forEach(inputField => {
            inputField.removeClass('is-invalid');
        });
    }

    // Set errors
    for (const [key, message] of Object.entries(errors)) {
        // Mark field as invalid
        fields[key].inputs.forEach(inputField => {
            inputField.addClass('is-invalid');
        });

        // Construct error message
        const errorMessageBlock = $(`
            <div class="error-msg-block flex-block">
                <span>${message}</span>
            </div>
        `);
        fields[key].block.append(errorMessageBlock);
    }
}
