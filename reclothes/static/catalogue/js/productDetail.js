const productId = $("#productId").attr("data-id");
const mainInfoBlock = $('#product-main-info-block');
const AddInfoBlock = $('#product-add-info-block');

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
  setTagsInfo(result.product.tags);
  setAdditionalInfo(result.attrs);
}

function setMainInfo(data) {
  mainInfoBlock.empty();
  const info = $(`
    <div class="flex-block">
      <a href="/product/${data.id}">Title: ${data.title}</a>
      <span>Type: ${data.product_type.name}</span>
      <span>Category: ${data.category.name}</span>
      <span>Price: ${data.regular_price}</span>
      <span>Description: ${data.description}</span>
      <span>Active: ${data.is_active}</span>
      <span>Quantity: ${data.quantity}</span>
      <span>Last update: ${data.last_update}</span>
      <span>Creation date: ${data.creation_date}</span>
    </div>
  `);
  mainInfoBlock.append(info);
}

function setTagsInfo(data) {
  const tagsInfo = $(`<div class="tags-block"></div>`);
  data.forEach(tag => {
    const tagBlock = $(`
      <div class="single-tag-block">
        <span>${tag.name}</span>
      </div>
    `);
    tagsInfo.append(tagBlock);
  });
  mainInfoBlock.append(tagsInfo);
}

function setAdditionalInfo(data) {
  AddInfoBlock.empty();
  data.forEach(item => {
    let info = $(`
        <span>${item.attribute.name} - ${item.value}</span>
    `);
    AddInfoBlock.append(info);
  });
}

getProductData();