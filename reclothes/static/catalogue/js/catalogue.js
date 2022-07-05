const apiUrl = "/api";
const catalogueUrl = `${apiUrl}/catalogue`;
const categoriesUrl = `${apiUrl}/category`;
const tagsUrl = `${apiUrl}/tag`;

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
    console.log("catalogue");
}

function setCategories(data) {
    console.log("categories");
}

function setTags(data) {
    console.log("tags");
}

getData(catalogueUrl, setCatalogue);
getData(categoriesUrl, setCategories);
getData(tagsUrl, setTags);