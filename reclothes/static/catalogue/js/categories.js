const subCategoriesBlock = $('#subcategories-block');


function getSubCategories(url, callback) {
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


// TODO: Fix this when get root or sub ones
function setSubCategories(data) {
    // Adding items
    data.roots.forEach(root => {
        root.category_tree.forEach(category => {
            const alink = $(`<button type="button" class="btn btn-link">${category.name}</button>`);
            alink.click(() => {handleCategoryClick(category.id);});
            const subCategoryBlock = $(`
                <div class="default-block"></div>
            `);
            subCategoryBlock.append(alink);
            subCategoriesBlock.append(subCategoryBlock);
        });
    });
}


function getURL() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('category_id');
    let url = rootCategoriesUrl.href;
    if (id !== '' && id !== null) {
        url = `${defaultCategoriesUrl}/${id}`;
    }
    return url;
}


const apiCallURL = getURL();
getSubCategories(apiCallURL, setSubCategories);
