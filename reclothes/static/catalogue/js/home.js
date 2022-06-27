function getHomeData() {
  $.ajax({
    url: '/api/product/get_home_products',
    method: 'GET',
    dataType: 'json',
    success: (result) => {
      console.log(result);
      const c1 = $(`<p>${result.hot_products[0].count}</p>`);
      const c2 = $(`<p>${result.best_products[0].avg_rate}</p>`);
      const c3 = $(`<p>${result.newest_products}</p>`);
      $('#best-products-block').append(c2);
      $('#hot-products-block').append(c1);
      $('#newest-products-block').append(c3);

    },
    error: (error) => {
      console.log(error);
    }
  });
}

getHomeData();
