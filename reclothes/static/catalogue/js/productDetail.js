const productId = $("#productId").attr("data-id");
const mainInfoBlock = $('#product-main-info-block');
const addInfoBlock = $('#product-add-info-block');
const topInfoBlock = $('#top-info-block');
const descrInfoBlock = $('#description-info-block');
const reviewsInfoBlock = $('#reviews-info-block');
const bottomInfoBlock = $('#bottom-info-block');
const noImgUrl = '/static/reclothes/images/empty.jpg';


function getProductData() {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: `/api/product/get_product_detail/${productId}`,
        headers: {"X-CSRFToken": csrftoken},
        method: 'GET',
        dataType: 'json',
        success: (result) => {
            console.log(result);
            displayProductInfo(result);
        },
        error: (error) => {
            console.log(error);
        }
    });
}

function displayProductInfo(result) {
    setMainInfo(result.product);
    setImages(result.images);
    setDescription(result.product.description);
    setAdditionalInfo(result.attrs);
    if (result.reviews.length > 0) {
        setReviewsInfo(result.reviews);
    }
}

function getAvailability(isActive, quantity) {
    // 1 - OK
    // 2 - Out of stock
    // 3 - Unavailable

    let active = 1;
    let text = "Add to cart";
    if (isActive) {
        if (quantity <= 0) {
            active = 2;
            text = "Out of stock";
        }
    } else {
        active = 3;
        text = "Unavailable";
    }
    return {
        active: active,
        text: text,
    };
}

function buildButton(availability) {
    const button = $(`
        <button id="add-to-cart-btn" type="button" class="btn btn-primary">
            ${availability.text}
        </button>
    `);
    if (availability.active !== 1) {
        button.prop('disabled', true);
    }
    return button;
}

function setMainInfo(data) {
    mainInfoBlock.empty();
    const info = $(`
        <div id="info-block">
            <div class="flex-block main-info">
                <div id="detail-title-block">
                    <span id="detail-title">${data.title}</span>
                </div>
                <div id="detail-price-block">
                    <span id="detail-price">${data.regular_price}$</span>
                </div>
            </div>
        </div>
    `);
    mainInfoBlock.append(info);

    // Add to cart button
    const availability = getAvailability(data.is_active, data.quantity);
    button = buildButton(availability);
    const detailPriceBlock = $('#detail-price-block');
    detailPriceBlock.append(button);

    setCategoriesInfo(data.category.category_tree, data.product_type);
    setTagsInfo(data.tags);
    setDatesInfo(data.last_update, data.creation_date);
}

function setCategoriesInfo(categories, type) {
    const categoriesBlock = $(`
        <div class="categories-block">
            <a href="#" class="category-link">Catalogue&nbsp;</a>
        </div>
    `);
    topInfoBlock.empty();
    categories.forEach(category => {
        const categoryBlock = $(`
            <div class="single-category-block">
                <span class="category-span">\> <a class="category-link" href="/category/${category.id}">${category.name}</a></span>
            </div>
        `);
        categoriesBlock.append(categoryBlock);
    });

    const typeBlock = $(`
        <div>
            <span>Type: <a href="/filter?product_type=${type.id}" class="category-link">${type.name}</a></span>
        </div>
    `);
    topInfoBlock.append(typeBlock);
    topInfoBlock.append(categoriesBlock);
}

function setTagsInfo(data) {
    const tagsInfo = $(`<div class="tags-block"></div>`);
    data.forEach(tag => {
        const tagBlock = $(`
            <div class="single-tag-block">
            <a href="#" class="tag">${tag.name}</a>
            </div>
        `);
        tagsInfo.append(tagBlock);
    });
    mainInfoBlock.append(tagsInfo);
}

function setDatesInfo(creationDate, lastUpdate) {
    const datesBlock = $(`
        <div class="dates-block">
            <span class="date-span">Creation date: ${formatDate(creationDate)}</span>
            <span class="date-span">Last update: ${formatDate(lastUpdate)}</span>
        </div>
    `);

    bottomInfoBlock.append(datesBlock);
}

function setImages(data) {
    const infoBlock = $('#info-block');
    const imagesBlock = $(`<div class="images-block"></div>`);
    let imgUrl = noImgUrl;
    let altText = "No image";
    // First image will always be feature image if exists
    if (data.length > 0) {
        imgUrl = data[0].image;
        altText = data[0].alt_text;
    }
    const image = $(`
        <img class="product-image" src="${imgUrl}" alt="${altText}"></img>
    `);
    imagesBlock.append(image);
    infoBlock.append(imagesBlock);
}

function setAdditionalInfo(data) {
    if (data.length == 0) {
        addInfoBlock.remove();
        return;
    }
    addInfoBlock.empty();
    const label = $(`<span class="block-label">Additional information</span>`);
    addInfoBlock.append(label);
    data.forEach(item => {
        let info = $(`
            <div class="attr-block">
                <span class="attr-span">${item.attribute.name}</span>
                <span class="attr-value-span">${item.value}</span>
            </div>
        `);
        addInfoBlock.append(info);
    });
}

function setDescription(description) {
    let text = description;
    if (description == "") {
        text = "No information given.";
    } 
    descrInfoBlock.empty();
    const label = $(`<span class="block-label">Description</span>`);
    descrInfoBlock.append(label);
    const descr = $(`
        <div>
            <p>${text}</p>
        </div>
    `);
    descrInfoBlock.append(descr);
}

function setReviewsInfo(data) {
    reviewsInfoBlock.empty();
    const label = $(`
        <span class="block-label">Reviews</span>
        <span class="grey-line"></span>
    `);
    reviewsInfoBlock.append(label);
    if (data.length == 0) {
        const emptyText = $(`<span>No reviews yet</span>`);
        reviewsInfoBlock.append(emptyText);
        return;
    }
    data.forEach(reviewData => {
        const line = $(`<span class="grey-line"></span>`);
        const rateBar = $(`<div class="rate-bar"></div>`);
        for (let i = 0; i < parseInt(reviewData.rating); i++) {
            const star = $(`<i class="d-flex justify-content-center align-items-center bi bi-star-fill rate-star"></i>`);
            rateBar.append(star);
        }
        for (let i = 0; i < 5 - parseInt(reviewData.rating); i++) {
            const star = $(`<i class="d-flex justify-content-center align-items-center bi bi-star rate-star"></i>`);
            rateBar.append(star);
        }
        const creationDate = formatDate(reviewData.creation_date);
        const userReviewInfo = $(`
            <div class="user-review-block">
                <div class="detail-review-user-block">
                    <img src="${noImgUrl}" class="user-avatar" />
                    <a href="#" class="review-username">${reviewData.user.username}</a>
                </div>
                
                <span class="review-date">${creationDate}</span>
            </div>
        `);
        const review = $(`
            <div class="review-block">
                <span class="review-comment-label">Comment</span>
                <span>${reviewData.text}</span>
            </div>
        `);
        reviewsInfoBlock.append(line);
        reviewsInfoBlock.append(userReviewInfo);
        reviewsInfoBlock.append(rateBar);
        reviewsInfoBlock.append(review);
        reviewsInfoBlock.append(line);
    });
}

getProductData();