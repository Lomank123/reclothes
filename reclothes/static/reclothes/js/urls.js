const baseUrl = 'http://127.0.0.1:8000';
const apiUrl = "/api";
const categoriesUrl = `${apiUrl}/category`;
const tagsUrl = `${apiUrl}/tag`;

const defaultCatalogueUrl = `${apiUrl}/catalogue`;
const catalogueUrl = getCatalogueUrl();

function getCatalogueUrl() {
    let url = new URL(defaultCatalogueUrl, baseUrl);
    const params = new URLSearchParams(window.location.search);
    params.forEach((value, key) => {
        url.searchParams.set(key, value);
    });
    return url;
}
