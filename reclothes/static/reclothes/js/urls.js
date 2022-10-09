const baseUrl = 'http://127.0.0.1:8000';
const apiUrl = "/api";

// Default api urls
const defaultOrderUrl = `${apiUrl}/order`;
const defaultUserUrl = `${apiUrl}/user`;
const defaultProductUrl = `${apiUrl}/product`;
const defaultCartUrl = `${apiUrl}/cart`;
const defaultCartItemUrl = `${apiUrl}/cart_item`;
const defaultTagsUrl = `${apiUrl}/tag`;
const defaultCategoriesUrl = `${apiUrl}/category`;
const defaultRootCategoriesUrl = `${defaultCategoriesUrl}/root`;
const defaultCatalogueDataUrl = `${defaultProductUrl}/catalogue`;
const defaultPaginatedCartItemsUrl = `${defaultCartItemUrl}/all_by_cart`;

// Products
const catalogueDataUrl = getUrlWithSearch(defaultCatalogueDataUrl);
const homeProductsUrl = `${defaultProductUrl}/home`;
// Categories
const categoriesUrl = getUrlWithSearch(defaultCategoriesUrl);
const rootCategoriesUrl = getUrlWithSearch(defaultRootCategoriesUrl);
const subCategoriesUrl = `${defaultCategoriesUrl}/sub`;
// Cart and cart items
const sessionCartUrl = `${defaultCartUrl}/session_cart`;
const headerCartItemsUrl = `${defaultCartItemUrl}/header`;
const changeCartItemQuantityUrl = `${defaultCartItemUrl}/change_quantity`;
const paginatedCartItemsUrl = getUrlWithSearch(defaultPaginatedCartItemsUrl);
// Orders
const orderFileUrl = `${defaultOrderUrl}/files`;
const myOrdersUrl = getUrlWithSearch(defaultOrderUrl);

// Non-api urls
const cataloguePageUrl = `${baseUrl}/catalogue`;
const cartPageUrl = `${baseUrl}/cart`;
const productDetailUrl = `${baseUrl}/product`;

const orderUrl = `${baseUrl}/order`;
const downloadFileUrl = `${orderUrl}/download`;

function getUrlWithSearch(defaultUrl) {
    let url = new URL(defaultUrl, baseUrl);
    const params = new URLSearchParams(window.location.search);
    params.forEach((value, key) => {
        url.searchParams.set(key, value);
    });
    return url;
}
