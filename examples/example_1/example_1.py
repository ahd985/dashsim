import json
import sys
sys.path.append("../../")
import dashsim


# Initialize DashSim
# Provide chart ids - these can be found in the template (html) file
dash = dashsim.DashSim()

# Build collector class for DashSim instantiation
class DataCollector(dashsim.DataCollectorMeta):
    def collect_data(self):
        df = self.read_csv('standard_n.csv', header=[0, 1, 2])
        # Collapse multi-column to one column
        df.columns = [', '.join(col).strip() for col in df.columns.values]

        for col in df.columns[1:]:
            trace = self.go.Scatter(x=df[df.columns[0]], y=df[col])
            self.plots.append([trace])

dash.set_collector(DataCollector)

# Run server
dash.start_server(port=8899)
