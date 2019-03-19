import argparse
import json
import os
from collections import defaultdict

import plotly.graph_objs as go
from plotly.offline import plot

"""
Structure of a K.json file, with K=[-1,3]:
{
    benchmarks: [
                    metadata: {name: float},
                    runs:   [
                                { metadata, warmups, values:[] } # values doesn't exist for the calibration runs
                            ]
                ]
    metadata: {resolution, python c flags, cpu count, and other uninteresting stuff}
    version: 1.0
} 
"""


def parse_args():
    parser = argparse.ArgumentParser(description='Visualize benchmark results')
    parser.add_argument('path', metavar='p', type=str, help='path of the results directory')
    args = parser.parse_args()
    return args


def get_files(dir_path):
    """
    :param dir_path: path of the results directory
    :return: names of json files inside the directory
    """
    if not os.path.isdir(dir_path):
        os.sys.exit('%s is not a directory' % dir_path)

    json_files = [file for file in os.listdir(dir_path) if file.endswith('.json')]
    if len(json_files) == 0:
        os.sys.exit('%s does not contain any json files' % dir_path)

    return [jf for jf in json_files]


def read_json(file):
    """
    :param file: path of a json file
    :return:
    """
    with open(file) as f:
        data = json.load(f)
    return data


def get_full_data(dir_path, files):
    """
    :param dir_path: path of directory holding the json files
    :param files: json files
    :return: dictionary with monitoring levels as keys. each key holds the content of its respective json file.
    """
    data = {}
    for file in files:
        key = int(os.path.splitext(file)[0])
        value = read_json(os.path.join(dir_path, file))
        data[key] = value
    return data


def get_visualization_data(full_data):
    """
    :param full_data: benchmark results from json files
    :return: dict of the form:
    {
        benchmark_name: { monitoring level: [runs]}
    }
    """
    data = defaultdict(lambda: defaultdict(list))
    for key in full_data.keys():
        benchmarks = full_data[key]['benchmarks']
        for b in benchmarks:
            name = b['metadata']['name']
            values = []
            runs = b['runs']
            for r in runs:
                if 'values' not in r:
                    continue
                values.extend(r['values'])
            data[name][key].extend(values)

    return data


def violin_plot(benchmark_data, benchmark_name, dir_path, max_val):
    data = []
    for k in sorted(benchmark_data.keys()):
        trace = {
            "type": 'violin',
            "x": [k]*len(benchmark_data[k]),
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
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename=os.path.join(dir_path, benchmark_name + '.html'))


def main():
    path = parse_args().path
    print("Violin plots of benchmark results from directory %s" % path)
    files = get_files(path)
    full_data = get_full_data(path, files)  # indexed by monitoring level
    vis_data = get_visualization_data(full_data)  # indexed by benchmark name
    max_val = max(max(vv) for v in vis_data.values() for vv in v.values())
    for benchmark in vis_data.keys():
        violin_plot(vis_data[benchmark], benchmark, path, max_val)


if __name__ == "__main__":
    main()
