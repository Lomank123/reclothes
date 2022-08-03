const baseUrl = 'http://127.0.0.1:8000';
const apiUrl = "/api";

const defaultTagsUrl = `${apiUrl}/tag`;
const defaultCategoriesUrl = `${apiUrl}/category`;
const defaultCatalogueUrl = `${apiUrl}/catalogue`;
const defaultRootCategoriesUrl = `${defaultCategoriesUrl}/root`;

const catalogueUrl = getUrlWithSearch(defaultCatalogueUrl);
const categoriesUrl = getUrlWithSearch(defaultCategoriesUrl);
const rootCategoriesUrl = getUrlWithSearch(defaultRootCategoriesUrl);
const subCategoriesUrl = `${defaultCategoriesUrl}/sub`;

const cataloguePageUrl = `${baseUrl}/catalogue`;

function getUrlWithSearch(defaultUrl) {
    let url = new URL(defaultUrl, baseUrl);
    const params = new URLSearchParams(window.location.search);
    params.forEach((value, key) => {
        url.searchParams.set(key, value);
    });
    return url;
}
