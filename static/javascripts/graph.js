var csv_data = [
  {
    key: "Temperature",
    values: [],
    'color': '#79C36A'
  },
  {
    key: "RelativeHumidity",
    values: [],
    'color': '#111111'
  },
];

var datatype_mapping = {
  0: "Temperature",
  1: "RelativeHumidity"
}

var datatype_index = {}

var initial = csv_data.length;
var remaining = initial;

for (var i=0; i<remaining; i++) {
  datatype_index[csv_data[i].key] = i;
}

function plot() {
  var chart;

  nv.addGraph(function() {
    chart = nv.models.lineChart();

    chart.title
   
    chart.xAxis
        .tickFormat(function(d) { return d3.time.format('%X')(new Date(d)); });

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
    console.log("Socket opened.")
    ws.send("Socket opened.");
  };
  ws.onmessage = function (evt) {
    var data = JSON.parse(evt.data);
    console.log(datatype_mapping, data.DataType);
    var type = datatype_mapping[data.DataType];
    var index = datatype_index[type];
    console.log(data, index);
    csv_data[index].values.push({x: data.Timestamp, y: data.Measurement});
    d3.select('#chart svg')
              .datum(csv_data)
              .transition().duration(500)
              .call(chart);
  };
}


// load csvs in parallel
for (var i=0; i<initial; i++) {
  (function(i) {
    var key = csv_data[i].key;
    d3.csv("/static/csvs/" + key + ".csv", function(error, data){
      data.forEach(function (d){
        console.log(datatype_mapping, i);
        var type = datatype_mapping[i];
        var index = datatype_index[type]
        csv_data[index].values.push({x: d.Timestamp, y: d.Measurement});
      })    

      remaining--;
      if (!remaining) {
        plot()
      }   
    });
  })(i);
}