function getHomeData() {
  $.ajax({
    url: '/api/product/get_home_products',
    method: 'GET',
    dataType: 'json',
    success: (result) => {
      console.log(result);
      setHomeData(result);
    },
    error: (error) => {
      console.log(error);
    }
  });
}

function setHomeData(result) {
  // Hot
  result.hot_products.forEach(product => {
    let info = $(`
      <div>
        <p>Type: ${product.type}</p>
        <p>Title: ${product.title}</p>
        <p>Price: ${product.regular_price}</p>
        <p>Purchases: ${product.purchases}</p>
      </div>
    `);
    $('#hot-products-block').append(info);
  });
  

  // Best
  result.best_products.forEach(product => {
    let info = $(`
      <div>
        <p>Type: ${product.type}</p>
        <p>Title: ${product.title}</p>
        <p>Price: ${product.regular_price}</p>
        <p>Rating: ${product.avg_rate}</p>
      </div>
    `);
    $('#best-products-block').append(info);
  });
  

  // Newest
  result.newest_products.forEach(product => {
    let info = $(`
      <div>
        <p>Type: ${product.type}</p>
        <p>Title: ${product.title}</p>
        <p>Price: ${product.regular_price}</p>
      </div>
    `);
    $('#newest-products-block').append(info);
  });
  

}


getHomeData();
