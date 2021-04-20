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
          result.data.name + ": " + result.data.market_data.price_usd.toString().slice(0, 12)
        );
        var price_usd = result.data.market_data.price_usd;
        var price_1h = result.data.market_data.percent_change_usd_last_1_hour;
        var price_24h = result.data.market_data.percent_change_usd_last_24_hours;
        var price_btc = result.data.market_data.price_btc;
        var price_eth = result.data.market_data.price_eth;

        var price_data = "" + result.data.symbol;
        try {
          price_data += "," + price_usd.toString().slice(0, 12);
        } catch (issue) {
          price_data += ", none";
          console.log("issue: " + issue);
        }
        try {
          price_data += "," + price_1h.toString().slice(0, 12);
        } catch (issue) {
          price_data += ", none";
          console.log("issue: " + issue);
        }
        try {
          price_data += "," + price_24h.toString().slice(0, 12);
        } catch (issue) {
          price_data += ", none";
          console.log("issue: " + issue);
        }
        try {
          price_data += "," + price_btc.toString().slice(0, 12);
        } catch (issue) {
          price_data += ", none";
          console.log("issue: " + issue);
        }
        try {
          price_data += "," + price_eth.toString().slice(0, 16);
        } catch (issue) {
          price_data += ", none";
          console.log("issue: " + issue);
        }
        updateDB(price_data);
      } catch (error) {
        console.log("oops..." + error);
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
