let productId = $("#productId").attr("data-id");

function getProductData() {
  const csrftoken = getCookie('csrftoken');
  $.ajax({
    url: `/api/product/get_product_detail/${productId}`,
    headers: {"X-CSRFToken": csrftoken},
    method: 'GET',
    dataType: 'json',
    success: (result) => {
      console.log(result);
    },
    error: (error) => {
      console.log(error);
    }
  });
}

getProductData();