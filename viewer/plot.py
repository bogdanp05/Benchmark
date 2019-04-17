import os

import plotly.graph_objs as go
from plotly.offline import plot


FONT = dict(size=18)


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
        title='%s benchmark' % benchmark_name,
        xaxis=dict(
            title="FMD monitoring level"
        ),
        yaxis=dict(
            title="response time (s)",
            range=[0, max_val]
        ),
        font=FONT
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
        title='%s benchmark' % benchmark_name,
        xaxis=dict(
            title="Measurements"
        ),
        yaxis=dict(
            title="response time (s)",
            range=[0, max_val]
        ),
        font=FONT
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, benchmark_name + '_line.html'))


def overhead_plot(stats_data, benchmark_name, dir_path):
    data = []
    for k in sorted(stats_data.keys()):
        if k == -1:
            pass
        trace = {
            "type": 'scatter',
            "x": list(stat['mean'] for stat in stats_data[-1]),
            "y": list(stat['mean'] - base['mean'] for stat in stats_data[k] for base in stats_data[-1]),
            "mode": 'lines',
            "name": k
        }
        data.append(trace)

    layout = go.Layout(
        title='%s benchmark' % benchmark_name,
        xaxis=dict(
            title="Base response time (s)"
        ),
        yaxis=dict(
            title="Overhead (s)",
        ),
        font=FONT
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, 'overhead_' + benchmark_name + '.html'))

