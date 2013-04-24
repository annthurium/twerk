WIDTH = HEIGHT = 500;

var P = function(x, y) {
  var point = [x, y];
  point.x = x;
  point.y = y;
  return point;
}

/*
var DATA = [
  [
    P(0, 40),
    P(250, 100),
    P(300, 78),
    P(400, 12)
  ],
  [
    P(0, 20),
    P(250, 30),
    P(300, 63),
    P(400, 98)
  ]
];
*/

function GenRandomData(num_layers, num_points) {
  x_transform = d3.scale.linear()
    .domain([0, num_points])
    .range([0, WIDTH]);
  y_transform = d3.scale.linear()
    .range([HEIGHT / num_layers, 0]);

  var layers = [];
  for (var i = 0; i != num_points; ++i) {
    var x = x_transform(i);
    for (var j = 0; j != num_layers; ++j) {
      if (i == 0) {
        // On the first point, add a new layer.
        layers.push([]);
      }

      layers[j].push(P(
        x,
        y_transform(Math.random())
      ));
    }
  }
  return layers;
}


DATA = GenRandomData(10, 50);

// creates a values accessor for each layer
var stacker = d3.layout.stack()
  .offset('wiggle')
  .order('inside-out');
var color = d3.scale.linear().range(["#a0a", "#f0e"]);
var area = d3.svg.area()
  .x0(function(d) { return d.y0; })
  .x1(function(d) { return d.y0 + d.y; })
  .y(function(d) { return d.x; })
  .interpolate('basis');


function draw() {
  var svg = d3.select("body")
    .append("svg")
    .attr("width", WIDTH)
    .attr("height", HEIGHT);

  svg.selectAll("path")
    .data(stacker(DATA))
    .enter()
      .append("path")
      .attr("d", area)
      .style("fill", function() { 
        return color(Math.random()); 
      });
}

addEventListener('load', draw, false);