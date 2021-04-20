var coins = document.getElementById("update_controller").value;
var coinsArr = coins.split(",");
var csrf = $("input[name=csrfmiddlewaretoken]").val();

for (coin of coinsArr) {
  $.ajax({
    url: "https://data.messari.io/api/v1/assets/" + coin + "/metrics",
    type: "get",
    success: function (result) {
      try {
        console.log(
          result.data.name + ": " + result.data.market_data.price_usd.toString().slice(0, -10)
        );
        updateDB(
          result.data.symbol +
            "," +
            result.data.market_data.price_usd.toString().slice(0, -10) +
            "," +
            result.data.market_data.percent_change_usd_last_1_hour.toString().slice(0, -10) +
            "," +
            result.data.market_data.percent_change_usd_last_24_hours.toString().slice(0, -10) +
            "," +
            result.data.market_data.price_btc.toString().slice(0, 12) +
            "," +
            result.data.market_data.price_eth.toString().slice(0, 16)
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
