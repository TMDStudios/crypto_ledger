var coins = document.getElementById("update_controller").value;
var coinsArr = coins.split(",");
var csrf = $("input[name=csrfmiddlewaretoken]").val();

for (coin of coinsArr) {
  $.ajax({
    url: "https://data.messari.io/api/v1/assets/" + coin + "/metrics",
    type: "get",
    success: function (result) {
      try {
        console.log(result.data.name + ": " + result.data.market_data.price_usd);
        updateDB(
          result.data.symbol +
            "," +
            result.data.market_data.price_usd +
            "," +
            result.data.market_data.percent_change_usd_last_1_hour +
            "," +
            result.data.market_data.percent_change_usd_last_24_hours +
            "," +
            result.data.market_data.price_btc +
            "," +
            result.data.market_data.price_eth
        );
      } catch (error) {
        console.log("oops");
      }
    },
  });
}

function updateDB(params) {
  console.log(params);
  $.ajax({
    url: "/api/set-prices/",
    type: "post",
    data: {
      coin_data: params,
      csrfmiddlewaretoken: csrf,
    },
    success: function (result) {
      console.log("price updated");
    },
  });
}
