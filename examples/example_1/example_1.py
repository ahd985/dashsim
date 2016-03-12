import json
import sys
sys.path.append("../../")


import dashsim
import pandas as pd


# Initialize DashSim
# Provide chart ids - these can be found in the template (html) file
dash = dashsim.DashSim()

# Build collector class for DashSim instantiation
class DataCollector(dashsim.DataCollectorMeta):
    def collect_data(self):
        df = self.read_csv('standard_n.csv', header=[0, 1, 2])
        df.columns = pd.MultiIndex.from_tuples([(col[0], col[2]) if 'Unnamed' in col[1] else
                      (', '.join(col[:2]), col[2]) for col in df.columns.values])
        df = df.set_index([df.columns.values[0]])
        df = df.sortlevel(level=1, axis=1)

        df = df.swaplevel(0, 1, axis=1)

        for unit, unit_df in df.groupby(level=0, axis=1):
            data = []
            layout = dict(
                xaxis=dict(title=', '.join(df.index.name)),
                yaxis=dict(title=unit),
            )
            for col in unit_df:
                data.append(self.go.Scatter(x=df.index.values, y=df[col], name=col[1]))

            # Note - max col_width is 12
            self.add_plot(dict(data=data, layout=layout), col_width=6)

dash.set_collector(DataCollector)

# Run server
dash.start_server(port=8899)
