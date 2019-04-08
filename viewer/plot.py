import os

import plotly.graph_objs as go
from plotly.offline import plot


def violin_plot(benchmark_data, benchmark_name, dir_path, max_val):
    data = []
    for k in sorted(benchmark_data.keys()):
        trace = {
            "type": 'violin',
            "x": [k] * len(benchmark_data[k]),
            "y": benchmark_data[k],
            "name": k,
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            }
        }
        data.append(trace)

    layout = go.Layout(
        title='%s micro' % benchmark_name,
        xaxis=dict(
            title="FMD monitoring level"
        ),
        yaxis=dict(
            title="response time (s)",
            range=[0, max_val]
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, benchmark_name + '_violin.html'))


def line_plot(benchmark_data, benchmark_name, dir_path, max_val):
    data = []
    for k in sorted(benchmark_data.keys()):
        trace = {
            "type": 'scatter',
            "x": list(range(len(benchmark_data[k]))),
            "y": sorted(benchmark_data[k], reverse=True),
            "mode": 'lines',
            "name": k
        }
        data.append(trace)

    layout = go.Layout(
        title='%s micro' % benchmark_name,
        xaxis=dict(
            title="Measurements"
        ),
        yaxis=dict(
            title="response time (s)",
            range=[0, max_val]
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, benchmark_name + '_line.html'))
