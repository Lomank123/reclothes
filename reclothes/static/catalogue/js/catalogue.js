function getData(url, callback) {
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
    console.log(catalogueUrl.href);
}

function setCategories(data) {
    console.log(categoriesUrl);
}

function setTags(data) {
    console.log(tagsUrl);
}

getData(catalogueUrl.href, setCatalogue);
// getData(categoriesUrl, setCategories);
getData(tagsUrl, setTags);