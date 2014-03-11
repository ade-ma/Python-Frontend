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

datatype_mapping = ["Temperature", "RelativeHumidity"]

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
    var type = datatype_mapping[data.DataType];
    var index = datatype_index[type];
    csv_data[index].values.unshift({x: data.Timestamp, y: data.Measurement});
    d3.select('#chart svg')
              .datum(csv_data)
              .transition().duration(0)
              .call(chart);
  };
}


// load csvs in parallel
for (var i=0; i<initial; i++) {
  (function(i) {
    var key = csv_data[i].key;
    $.get("/data/" + key, function(data){
      data = JSON.parse(data);
      console.log(data);
      data.forEach(function (tuple){
        var type = datatype_mapping[i];
        var index = datatype_index[type]
        csv_data[index].values.push({x: tuple[0], y: tuple[1]});
      })    

      remaining--;
      if (!remaining) {
        plot()
      }   
    });
  })(i);
}