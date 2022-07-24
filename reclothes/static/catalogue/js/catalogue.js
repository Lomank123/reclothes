const catalogueBlock = $('#catalogue-block');
const productsBlock = $('#products-block');


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
            //console.log(error);
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

    firstButton.unbind().click(() => { getCatalogueData(paginationData.first, setCatalogue); });
    previousButton.unbind().click(() => { getCatalogueData(paginationData.previous, setCatalogue); });
    nextButton.unbind().click(() => { getCatalogueData(paginationData.next, setCatalogue); });
    lastButton.unbind().click(() => { getCatalogueData(paginationData.last, setCatalogue); });

    console.log("Pagination set!");
}

function setCategories(data) {
    console.log(categoriesUrl);
}

function setTags(data) {
    console.log(tagsUrl);
}

getCatalogueData(catalogueUrl.href, setCatalogue);
// getCatalogueData(categoriesUrl, setCategories);
// getCatalogueData(tagsUrl, setTags);