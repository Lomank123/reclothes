const baseUrl = 'http://127.0.0.1:8000';
const apiUrl = "/api";

const defaultProductUrl = `${apiUrl}/product`;
const defaultCartUrl = `${apiUrl}/cart`;
const defaultCartItemUrl = `${apiUrl}/cart_item`;
const defaultTagsUrl = `${apiUrl}/tag`;
const defaultCategoriesUrl = `${apiUrl}/category`;
const defaultCatalogueUrl = `${apiUrl}/catalogue`;
const defaultRootCategoriesUrl = `${defaultCategoriesUrl}/root`;
const defaultCatalogueDataUrl = `${defaultCatalogueUrl}/data`;
const defaultPaginatedCartItemsUrl = `${defaultCartItemUrl}/all_by_cart`;

const catalogueUrl = getUrlWithSearch(defaultCatalogueUrl);
const catalogueDataUrl = getUrlWithSearch(defaultCatalogueDataUrl);
const categoriesUrl = getUrlWithSearch(defaultCategoriesUrl);
const rootCategoriesUrl = getUrlWithSearch(defaultRootCategoriesUrl);
const paginatedCartItemsUrl = getUrlWithSearch(defaultPaginatedCartItemsUrl);
const subCategoriesUrl = `${defaultCategoriesUrl}/sub`;
const cartFromSessionUrl = `${defaultCartUrl}/fetch_from_session`;
const homeProductsUrl = `${defaultProductUrl}/fetch_home_products`;
// Cart and cart items
const sessionCartUrl = `${defaultCartUrl}/session_cart`;
const headerCartItemsUrl = `${defaultCartItemUrl}/header`;
const changeCartItemQuantityUrl = `${defaultCartItemUrl}/change_quantity`;


const cataloguePageUrl = `${baseUrl}/catalogue`;
const cartPageUrl = `${baseUrl}/cart`;

function getUrlWithSearch(defaultUrl) {
    let url = new URL(defaultUrl, baseUrl);
    const params = new URLSearchParams(window.location.search);
    params.forEach((value, key) => {
        url.searchParams.set(key, value);
    });
    return url;
}
