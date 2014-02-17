d3.csv("/static/csvs/data.csv", function(error, data){

  console.log(data)
  var csv_data = [
    {
      key: "Temperature",
      values: [],
      'color': '#79C36A'
    },
    {
      key: "Humidity",
      values: [],
      'color': '#599AD3'
    }
  ];

  data.slice(0, 1600).forEach(function (d){
    console.log(d);
    csv_data[0].values.push({x: Date.parse(d.Timestamp), y: d.Temperature});
    csv_data[1].values.push({x: Date.parse(d.Timestamp), y: d.Humidity});
  })       

  var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

  nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart();

    chart.title
   
    chart.xAxis
        .tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); });

    chart.x2Axis
        .tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); });
   
    chart.yAxis
        .tickFormat(d3.format(',.2f'));
   
    chart.y2Axis
        .tickFormat(d3.format(',.2f'));
   
    d3.select('#chart svg')
        .datum(csv_data)
      .transition().duration(500)
        .call(chart);
   
    nv.utils.windowResize(chart.update);
   
    return chart;
  });

});
 