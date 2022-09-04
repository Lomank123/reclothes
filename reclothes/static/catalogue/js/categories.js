const subCategoriesBlock = $('#subcategories-block');
let isSubCategories = false;


function handleCategoryClick(id) {
    const params = new URLSearchParams(window.location.search);
    params.set('category_id', id);
    window.location.search = params.toString();
}


function setCategories(data) {
    if (isSubCategories) {
        const subCategories = data.items[0].category_tree;
        if (subCategories.length == 0) {
            window.location.replace(`${cataloguePageUrl}${window.location.search}`);
            return;
        }
        displayCategories(subCategories);
    } else {
        // display root categories
        displayCategories(data.items);
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


function getURL() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('category_id');
    let url = rootCategoriesUrl.href;
    if (id !== '' && id !== null) {
        url = `${subCategoriesUrl}/${id}`;
        isSubCategories = true;
    }
    return url;
}


$(window).on('load', async () => {
    const apiCallURL = getURL();
    const categories = await ajaxCall(apiCallURL);
    if ('detail' in categories) {
        console.log("Error occured!");
        return;
    };
    setCategories(categories.data);
});
