import json
import os
import sys
sys.path.append("../../")
sys.path.append('/Users/Alex/Documents/Python Projects/ssv')

import dashsim
import numpy as np
from ssv.ssv import SSV
import pandas as pd


# Initialize DashSim
# Provide chart ids - these can be found in the template (html) file
dash = dashsim.DashSim()


# Build collector class for DashSim instantiation
class DataCollector(dashsim.DataCollectorMeta):
    def collect_data(self):
        # Start with SSV
        data = pd.read_csv('standard_n.csv', skiprows=[2], header=[0, 1])
        data.columns = [', '.join(col) if i > 0 else col[0] for i, col in enumerate(data.columns)]

        # Initiate and hook up SSV model
        ssv_model = SSV.create_vis(data['Time'], 'seconds', 'example_1.svg',
                                   title="CFAST Example", font_size=10)

        gas_color_scale = ['#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026']
        gas_color_levels = np.linspace(min(data['Upper Layer Temperature, Comp 2']),
                                       max(data['Upper Layer Temperature, Comp 3']), 5)

        # Add nodes
        for i in range(1, 4):
            data['Layer Height Upper, Comp %d' % i] = 3.0
            node = ssv_model.add_element('cell', 'node-%d' % i, 'Node %d' % i, cell_report_id='node-%d-report' % i)
            node.add_condition('zonal_y', description='Zone Heights', unit='m',
                               data_2d=data[['Layer Height, Comp %d' % i, 'Layer Height Upper, Comp %d' % i]],
                               data_dynamic_2d=data[
                                   ['Lower Layer Temperature, Comp %d' % i,
                                    'Upper Layer Temperature, Comp %d' % i]],
                               color_scale=gas_color_scale,
                               color_levels=gas_color_levels,
                               max_height=3, description_dynamic='Zone Temperatures', unit_dynamic='C',
                               min_height=0, section_label='Zone')
            node.add_condition('info', data=data[['Pressure, Comp %d' % i]], description='Pressure', unit='Pa')

            if i == 1:
                node.add_condition('info', data=data[['HRR, bunsen']], description='HRR', unit='W')
            elif i == 2:
                node.add_condition('info', data=data[['HRR, Wood_Wall']], description='HRR', unit='W')

        # Add fires
        fire_1 = ssv_model.add_element('toggle', 'fire-1', 'Fire 1')
        fire_1.add_condition('show_hide', data=data['HRR, bunsen'])
        fire_2 = ssv_model.add_element('toggle', 'fire-2', 'Fire 2')
        fire_2.add_condition('show_hide', data=data['HRR, Wood_Wall'])

        # Show gas color scale
        ssv_model.add_element('colorscale', 'color-scale', 'Gas Temperature (C)',
                              color_scale=gas_color_scale,
                              color_levels=gas_color_levels)

        self.add_visualization(ssv_model, col_width=6, height_mult=1)

        # Plotly plots
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
            self.add_visualization(dict(data=data, layout=layout), col_width=6, height_mult=1)

dash.set_collector(DataCollector)

# Run server
dash.start_server(port=8899)
