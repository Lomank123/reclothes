const catalogueBlock = $('#catalogue-block');
const productsBlock = $('#products-block');
const applyButton = $('#apply-filters-btn');
applyButton.click(setFilterData);
const searchButton = $('#search-btn');
searchButton.click(setSearchData);


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
    // Set pagination text
    const pageText = $('#pagination-text');
    pageText.text(`${paginationData.number} of ${paginationData.num_pages}`);

    // Set buttons
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


function setSearchData() {
    let searchData = {
        'search': $('#search-input').val(),
    }
    handleFilter(searchData);
}


function setFilterData() {
    let filterData = {
        'price_from': $('#price-from-input').val(),
        'price_to': $('#price-to-input').val(),
    }
    handleFilter(filterData);
}


function handleFilter(filterData) {
    const newUrl = new URL(catalogueUrl.href);
    for (const [key, value] of Object.entries(filterData)) {
        if (value !== '' && value !== null) {
            newUrl.searchParams.set(key, value);
        } else {
            newUrl.searchParams.delete(key);
        }
    }

    // Reset page count
    newUrl.searchParams.delete('page');

    handleFilterClick(newUrl);
}


function setFilters() {
    const params = new URLSearchParams(window.location.search);
    $('#price-from-input').val(params.get('price_from'));
    $('#price-to-input').val(params.get('price_to'));
    // Search
    $('#search-input').val(params.get('search'));
}


getCatalogueData(catalogueUrl.href, setCatalogue);
setFilters();
