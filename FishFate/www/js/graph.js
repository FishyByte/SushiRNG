/**
 * Created by asakawa on 7/19/16.
 */
var trace = {
  x: [123, 232, 12, 53, 34, 5],
  y: [162, 246, 105, 201, 178],
  mode: 'markers',
  type: 'scatter',
  marker: { size: 4 }
};


var data = [ trace ];

var layout = {
  xaxis: {
    autotick: false,
    title: 'x',
    tick0: 0,
    dtick: 32,
    range: [0, 256]
  },
  yaxis: {
    autotick: false,
    title: 'y',
    tick0: 0,
    dtick: 32,
    range: [0, 256]
  },
  showlegend: false,
  title:'Scatter Plot of Generated Data From Fish Tank '
};

Plotly.newPlot(document.getElementById('myDiv'), data, layout, {displayModeBar: false});
