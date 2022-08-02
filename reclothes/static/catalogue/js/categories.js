const subCategoriesBlock = $('#subcategories-block');
let isSubCategories = false;


function getCategories(url, callback) {
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
        url = `${defaultCategoriesUrl}/${id}`;
        isSubCategories = true;
    }
    return url;
}


const apiCallURL = getURL();
getCategories(apiCallURL, setCategories);
