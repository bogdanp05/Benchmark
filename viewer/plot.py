import os

import plotly.graph_objs as go
from plotly.offline import plot

BASE = '-1'
SECONDS = False
FONT = dict(size=13)
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


def violin_plot_custom(benchmark_data, benchmark_name, dir_path, max_val):
    data = []
    keys = ['0', '1k', '5k', '10k', '50k', '100k']
    for idx, k in enumerate(keys):
        trace = {
            "type": 'violin',
            "x": [idx] * len(benchmark_data[k]),
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
            title="Endpoint previous hits",
            ticktext=keys,
            tickvals=[idx for idx,_ in enumerate(keys)]
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


def get_comparison_trace(comparison_data, k, x, factor):
    if not comparison_data:
        return None
    overheads = []
    deviations = []
    base_stats = comparison_data[BASE]
    monitored_stats = comparison_data[k]
    base_stats, monitored_stats = (list(s) for s in zip(*sorted(zip(base_stats, monitored_stats),
                                                                key=lambda pair: pair[0]['mean'])))
    for idx, dur in enumerate(base_stats):
        overheads.append((monitored_stats[idx]['mean'] - base_stats[idx]['mean']) * factor)
        deviations.append(monitored_stats[idx]['std'] * factor)
    comparison_trace = {
        "type": 'scatter',
        "x": x,
        "y": overheads,
        "error_y": {
            "type": 'data',
            "array": deviations,
            "visible": True
        },
        "mode": 'lines+markers',
        "name": str(k) + '(old)',
        # "line": {"color": COLORS[int(k) + 1 + 5]}
        "line": {"color": COLORS[2 + 1 + 5]}
    }
    return comparison_trace


def overhead_plot(stats_data, benchmark_name, dir_path, comparison_data=None):
    data = []
    factor = 1 if SECONDS else 1000
    addition = '(new)' if comparison_data else ''
    for k in sorted(stats_data.keys()):
        if k == BASE:
            continue
        overheads = []
        deviations = []
        base_stats = stats_data[BASE]
        monitored_stats = stats_data[k]
        base_stats, monitored_stats = (list(s) for s in zip(*sorted(zip(base_stats, monitored_stats),
                                                                    key=lambda pair: pair[0]['mean'])))
        for idx, dur in enumerate(base_stats):
            overheads.append((monitored_stats[idx]['mean'] - base_stats[idx]['mean'])*factor)
            deviations.append(monitored_stats[idx]['std'] * factor)
        x = [bs['mean'] * factor for bs in base_stats]
        trace_ov = {
                        "type": 'scatter',
                        "x": x,
                        "y": overheads,
                        "error_y": {
                                    "type": 'data',
                                    "array": deviations,
                                    "visible": True
                                    },
                        "mode": 'lines+markers',
                        "name": str(k) + addition,
                        "line": {"color": COLORS[int(k)+1]}
                    }

        data.append(trace_ov)
        comparison_trace = get_comparison_trace(comparison_data, k, x, factor)
        if comparison_trace:
            data.append(comparison_trace)

    unit = 'seconds' if SECONDS else 'ms'
    layout = go.Layout(
        title='%s benchmark' % benchmark_name,
        xaxis=dict(
            title="Base response time (%s)" % unit
        ),
        yaxis=dict(
            title="Overhead (%s)" % unit
        ),
        font=FONT,
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, 'overhead_' + benchmark_name + '.html'))
