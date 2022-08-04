const productsBlock = $('#products-block');
const tagsBlock = $('#tags-block');
const mainLabel = $('#catalogue-main-label');

const searchParams = new URLSearchParams(window.location.search);

// Buttons
const applyButton = $('#apply-filters-btn');
applyButton.click(applyFilters);

const discardButton = $('#discard-filters-btn');
discardButton.click(discardFilters);
if (window.location.search !== "") {
    discardButton.prop('disabled', false);
}

const searchButton = $('#search-btn');
searchButton.click(applySearch);


function getCurrentCategory() {
    const categoryId = searchParams.get('category_id');
    if (categoryId !== null) {
        const currentCategoryUrl = `${defaultCategoriesUrl}/${categoryId}`;
        ajaxGet(currentCategoryUrl, setCurrentCategory);
    }
}


function setCurrentCategory(data) {
    mainLabel.text(data.name);
}


function ajaxGet(url, callback) {
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


function setData(data) {
    setTags(data.popular_tags);
    setCatalogue(data.products.results);
    setPagination(data.products);
}


function setCatalogue(data) {
    // Cleaning block
    productsBlock.empty();
    // Adding items
    data.forEach(product => {
        const productBlock = $(`
            <div class="default-block">
                <a href="/product/${product.id}">${product.title}</a>
                <span>Price: ${product.regular_price}</span>
            </div>
        `);
        productsBlock.append(productBlock);
    });
}


function setTags(data) {
    if (data.length == 0) {
        tagsBlock.hide();
    }
    data.forEach(tag => {
        const tagButton = $(`<button type="button" class="btn btn-link tag">${tag.name}</button>`);
        tagButton.click(() => { handleTagClick(tag.id); });
        const tagBlock = $(`<div></div>`);
        tagBlock.append(tagButton);
        tagsBlock.append(tagBlock);
    });
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


function setFilters() {
    $('#price-from-input').val(searchParams.get('price_from'));
    $('#price-to-input').val(searchParams.get('price_to'));
    // Search
    $('#search-input').val(searchParams.get('search'));
}


function applySearch() {
    let searchData = {
        'search': $('#search-input').val(),
    }
    handleFilter(searchData);
}


function handleTagClick(tagId) {
    searchParams.set('tags', tagId);
    searchParams.delete('page');
    window.location.search = searchParams.toString();
}


function handleFilterClick(url) {
    const apiURL = new URL(url);
    window.location.search = apiURL.searchParams.toString();
}


function handleFilter(filterData) {
    const newUrl = new URL(catalogueDataUrl.href);
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


function applyFilters() {
    let filterData = {
        'price_from': $('#price-from-input').val(),
        'price_to': $('#price-to-input').val(),
    }
    handleFilter(filterData);
}


function discardFilters() {
    for (const [key, value] of searchParams.entries()) {
        if (key !== 'category_id') {
            searchParams.delete(key);
        }
    }
    window.location.search = searchParams.toString();
}


// Get catalogue data
ajaxGet(catalogueDataUrl.href, setData);
// Get current category data if exists
getCurrentCategory();
setFilters();
