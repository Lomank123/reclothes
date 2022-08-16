function handlePaginationClick(url) {
    const apiURL = new URL(url);
    window.location.search = apiURL.searchParams.toString();
}


function setPagination(data) {
    if (data.results.length == 0) {
        paginationBlock.hide();
        return;
    }
    // Set pagination text
    const pageText = $('#pagination-text');
    pageText.text(`${data.number} of ${data.num_pages}`);

    // Set buttons
    const firstButton = $('#first-btn');
    const previousButton = $('#previous-btn');
    const nextButton = $('#next-btn');
    const lastButton = $('#last-btn');

    firstButton.prop('disabled', data.first === null);
    previousButton.prop('disabled', data.previous === null);
    nextButton.prop('disabled', data.next === null);
    lastButton.prop('disabled', data.last === null);

    // .unbind() to prevent multiple click events
    firstButton.unbind().click(() => { handlePaginationClick(data.first); });
    previousButton.unbind().click(() => { handlePaginationClick(data.previous); });
    nextButton.unbind().click(() => { handlePaginationClick(data.next); });
    lastButton.unbind().click(() => { handlePaginationClick(data.last); });
}
