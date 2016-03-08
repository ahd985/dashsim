$(document).ready(function() {
  render_charts();
});

function render_charts() {
    var layout = {
      title:'Line and Scatter Plot'
    };
    for (var chart_id in data) {
        Plotly.newPlot(chart_id, data[chart_id], layout);
    }
}