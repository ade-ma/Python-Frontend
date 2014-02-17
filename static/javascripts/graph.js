d3.csv("/static/csvs/data.csv", function(error, data){

  console.log(data)
  var csv_data = [
    {
      key: "Measurement",
      values: [],
      'color': '#79C36A'
    },
  ];

  data.slice(0, 1600).forEach(function (d){
    csv_data[0].values.push({x: Date.parse(d.Timestamp), y: d.Measurement});
  })       

  var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;
  var chart;

  nv.addGraph(function() {
    chart = nv.models.lineChart();

    chart.title
   
    chart.xAxis
        .tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); });

    chart.yAxis
        .tickFormat(d3.format(',.2f'));
   
    d3.select('#chart svg')
        .datum(csv_data)
      .transition().duration(500)
        .call(chart);
   
    nv.utils.windowResize(chart.update);
   
    return chart;
  });

  var ws = new WebSocket("ws://localhost:8888/ws");
  ws.onopen = function() {
     ws.send("Socket opened.");
  };
  ws.onmessage = function (evt) {
    var data = JSON.parse(evt.data)
    csv_data[0].values.push({x: Date.parse(data.Timestamp), y: data.Measurement});
    d3.select('#chart svg')
              .datum(csv_data)
              .transition().duration(500)
              .call(chart);
  };
});