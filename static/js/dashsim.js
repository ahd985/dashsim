window.onresize = function() {
    Plotly.d3.selectAll('.plotly-graph-div').each(function() {Plotly.Plots.resize(this)})
};