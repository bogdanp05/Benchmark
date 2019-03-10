import json
import os
from collections import defaultdict

import plotly.graph_objs as go
from plotly.offline import plot

from visualize import RESULTS

# TODO: force user to input path
PATH = RESULTS + '190308_15:53:40/'

"""
Structure of a K.json, with K=[-1,3]:
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


def get_files(dir_path):
    """
    :param dir_path: path of the results directory
    :return: names of json files inside the directory
    """
    if not os.path.isdir(dir_path):
        os.sys.exit('%s is not a directory' % dir_path)

    json_files = [file for file in os.listdir(PATH) if file.endswith('.json')]
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

    print(data.keys())
    # benchmarks = data['benchmarks']
    # for b in benchmarks:
    #     print(b['metadata']['name'])
    #     runs = b['runs']
    #     for r in runs:
    #         print(r)
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
        value = read_json(dir_path + file)
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


def violin_plot(benchmark_data, benchmark_name):
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
            title="response time (s)"
            # type='log'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig)


def main():
    print("Violin plots of benchmark results from directory %s" % PATH)
    files = get_files(PATH)
    full_data = get_full_data(PATH, files)  # indexed by monitoring data
    vis_data = get_visualization_data(full_data)
    for benchmark in vis_data.keys():
        violin_plot(vis_data[benchmark], benchmark)


if __name__ == "__main__":
    main()
