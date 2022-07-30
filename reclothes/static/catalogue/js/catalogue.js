const catalogueBlock = $('#catalogue-block');
const productsBlock = $('#products-block');


function handleFilterClick(url) {
    const apiURL = new URL(url);
    window.location.search = apiURL.searchParams.toString();
}


function getCatalogueData(url, callback) {
    $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
        success: (result) => {
            console.log(result);
            callback(result);
        },
        error: (error) => {
            console.log(error);
        },
    });
}


function setCatalogue(data) {
    // Cleaning block
    productsBlock.empty();
    // Adding items
    data.results.forEach(product => {
        const productBlock = $(`
            <div class="default-block">
                <a href="/product/${product.id}">${product.title}</a>
                <span>Price: ${product.regular_price}</span>
            </div>
        `);
        productsBlock.append(productBlock);
    });
    setPagination(data);
}


function setPagination(paginationData) {
    const firstButton = $('#first-btn');
    const previousButton = $('#previous-btn');
    const nextButton = $('#next-btn');
    const lastButton = $('#last-btn');

    firstButton.prop('disabled', paginationData.first === null);
    previousButton.prop('disabled', paginationData.previous === null);
    nextButton.prop('disabled', paginationData.next === null);
    lastButton.prop('disabled', paginationData.last === null);

    // .unbind() to prevent multiple click events
    firstButton.unbind().click(() => { handleFilterClick(paginationData.first); });
    previousButton.unbind().click(() => { handleFilterClick(paginationData.previous); });
    nextButton.unbind().click(() => { handleFilterClick(paginationData.next); });
    lastButton.unbind().click(() => { handleFilterClick(paginationData.last); });
}


getCatalogueData(catalogueUrl.href, setCatalogue);
