import os

import plotly.graph_objs as go
from plotly.offline import plot

FONT = dict(size=18)
COLORS = ['rgb(31, 119, 180)',  # muted blue
          'rgb(255, 127, 14)',  # safety orange
          'rgb(44, 160, 44)',  # cooked asparagus green
          'rgb(214, 39, 40)',  # brick red
          'rgb(148, 103, 189)',  # muted purple
          'rgb(140, 86, 75',  # chestnut brown
          'rgb(227, 119, 194)',  # raspberry yogurt pink
          'rgb(127, 127, 127)',  # middle gray
          'rgb(188, 189, 34)',  # curry yellow-green
          'rgb(23, 190, 207)'   # blue-teal]
          ]


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
    base = -1
    durations = sorted(list(stat['mean'] * 1000 for stat in stats_data[base]))
    for k in sorted(stats_data.keys()):
        if k == base:
            continue
        overheads = []
        deviations = []
        for idx, base_stats in enumerate(stats_data[base]):
            base_mean = base_stats['mean']
            ov = stats_data[k][idx]['mean'] - base_mean
            overheads.append(ov*1000)
            overheads.sort()
            deviations.append((stats_data[k][idx]['std'] - stats_data[base][idx]['std'])*1000)
        trace_ov = {
                        "type": 'scatter',
                        "x": durations,
                        "y": overheads,
                        "error_y": {
                                    "type": 'data',
                                    "array": deviations,
                                    "visible": True
                                    },
                        "mode": 'lines+markers',
                        "name": k,
                        "line": {"color": COLORS[k+1]}
                    }

        data.append(trace_ov)

    layout = go.Layout(
        title='%s benchmark' % benchmark_name,
        xaxis=dict(
            title="Base response time (ms)"
        ),
        yaxis=dict(
            title="Overhead (ms)",
        ),
        font=FONT
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, 'overhead_' + benchmark_name + '.html'))
