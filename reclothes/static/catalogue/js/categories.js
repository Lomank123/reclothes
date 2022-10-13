const subCategoriesBlock = $('#subcategories-block');
const params = new URLSearchParams(window.location.search);


function handleCategoryClick(id) {
    params.set('category_id', id);
    // This will reload the page
    window.location.search = params.toString();
}


function isRootCategories() {
    const categoryId = params.get('category_id');
    return categoryId === null;
}


function setCategories(categories) {
    if (isRootCategories()) {
        displayCategories(categories);
    } else {
        // Display sub categories or redirect to catalogue page
        const subCategories = categories[0].category_tree;
        if (subCategories.length == 0) {
            window.location.replace(`${cataloguePageUrl}${window.location.search}`);
        }
        displayCategories(subCategories);
    }
}


function displayCategories(categories) {
    categories.forEach(category => {
        const alink = $(`<button type="button" class="btn btn-link">${category.name}</button>`);
        const subCategoryBlock = $(`<div class="default-block"></div>`);
        alink.click(() => {handleCategoryClick(category.id);});
        subCategoryBlock.append(alink);
        subCategoriesBlock.append(subCategoryBlock);
    });
}


$(window).on('load', async () => {
    const url = `${defaultCategoriesUrl}${window.location.search}`;
    const response = await ajaxCall(url);
    setCategories(response.detail.categories);
});
