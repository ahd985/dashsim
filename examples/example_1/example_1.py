import json
import sys
sys.path.append("../../")
import dashsim

# Initialize DashSim
# Provide chart ids - these can be found in the template (html) file
dash = dashsim.DashSim()

# Add chart data
# Pre-generated data
trace1 = {
  'x': [1, 2, 3, 4],
  'y': [10, 15, 13, 17],
  'type': 'scatter'
}
trace2 = {
  'x': [1, 2, 3, 4],
  'y': [16, 5, 11, 9],
  'type': 'scatter'
}
data = [trace1, trace2]

dash.add_chart('chart-1')
dash.update_chart_data('chart-1', data)

# Run server
dash.start_server(port=8894)
