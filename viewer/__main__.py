import argparse
import json
import os
from collections import defaultdict
from math import sqrt

from viewer.plot import violin_plot, line_plot, overhead_plot
from viewer.statistics import linear_regression

"""
Structure of a K.json file, with K={-1,0,1,2,3}:
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
    parser = argparse.ArgumentParser(description='Visualize micro results')
    parser.add_argument('--path', metavar='p', nargs='+', help='paths of the results directories')
    # parser.add_argument('--path', metavar='p', type=str, help='path of the results directory')
    parser.add_argument('--type', metavar='t', type=str, default='violin',
                        help='type of visualization. options: violin, line, or both. default: violin')
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
    :param full_data: micro results from json files
    :return: dict of the form:
    {
        benchmark_name: { monitoring level: [runs]}
    }
    """
    data = defaultdict(lambda: defaultdict(list))
    for key in full_data.keys():
        benchmarks = full_data[key]['benchmarks']
        for b in benchmarks:
            name = b['metadata']['name'] if len(benchmarks) != 1 else full_data[key]['metadata']['name']
            values = []
            runs = b['runs']
            for r in runs:
                if 'values' not in r:
                    continue
                values.extend(r['values'])
            data[name][key].extend(values)

    return data


def build_violin_plots(path, vis_data, max_val):
    print("Generating violin plots of micro results from directory %s" % path)
    for benchmark in vis_data.keys():
        violin_plot(vis_data[benchmark], benchmark, path, max_val)


def build_line_plots(path, vis_data, max_val):
    print("Generating line plots of micro results from directory %s" % path)
    for benchmark in vis_data.keys():
        line_plot(vis_data[benchmark], benchmark, path, max_val)


def build_plots(path, chart_type, vis_data):
    max_val = max(max(vv) for v in vis_data.values() for vv in v.values())
    if chart_type == 'line':
        build_line_plots(path, vis_data, max_val)
    elif chart_type == 'violin':
        build_violin_plots(path, vis_data, max_val)
    elif chart_type == 'both':
        build_violin_plots(path, vis_data, max_val)
        build_line_plots(path, vis_data, max_val)
    else:
        print("'%s' is not a valid plot type. Use 'python -m viewer --help' to see valid options." % chart_type)


def get_stats(full_stats, vis_data):
    """
    :param vis_data: data of the form:
        {
            benchmark_name: { monitoring level: [runs]}
        }
    :param full_stats: empty dict OR dict of the form:
        {
            benchmark_name: { monitoring level: [{mean, std}]}
        }
    """
    for bm in vis_data.keys():
        if bm not in full_stats.keys():
            full_stats[bm] = {}
        for ml in vis_data[bm].keys():
            runs = vis_data[bm][ml]
            mean = sum(runs)/len(runs)
            std = sqrt(sum((r - mean) ** 2 for r in runs) / len(runs))
            if ml not in full_stats[bm]:
                full_stats[bm][ml] = []
            full_stats[bm][ml].append({'mean': mean, 'std': std})


def get_multiple_measurements(result_dirs, dir_path):
    full_stats = {}
    for rd in result_dirs:
        files = get_files(rd)
        full_data = get_full_data(rd, files)
        vis_data = get_visualization_data(full_data)
        get_stats(full_stats, vis_data)
    for bm in full_stats.keys():
        linear_regression(full_stats[bm], bm)
        overhead_plot(full_stats[bm], bm, dir_path)


def main():
    args = parse_args()
    if args.path:
        if len(args.path) == 1:
            path = args.path[0]
            files = get_files(path)
            full_data = get_full_data(path, files)  # indexed by monitoring level
            vis_data = get_visualization_data(full_data)  # indexed by micro name
            build_plots(path, args.type, vis_data)
        else:
            get_multiple_measurements(args.path, args.path[0])
    else:
        print('No results directory was specified.')


if __name__ == "__main__":
    main()
