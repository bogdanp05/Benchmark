import argparse
import json
import os
from collections import defaultdict

from viewer.plot import violin_plot, line_plot

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
    parser.add_argument('--results', metavar='r', nargs='+', help='paths of the results directories')
    parser.add_argument('--path', metavar='p', type=str, help='path of the results directory')
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


def build_violin_plots(args, vis_data, max_val):
    print("Generating violin plots of micro results from directory %s" % args.path)
    for benchmark in vis_data.keys():
        violin_plot(vis_data[benchmark], benchmark, args.path, max_val)


def build_line_plots(args, vis_data, max_val):
    print("Generating line plots of micro results from directory %s" % args.path)
    for benchmark in vis_data.keys():
        line_plot(vis_data[benchmark], benchmark, args.path, max_val)


def build_plots(args, vis_data):
    max_val = max(max(vv) for v in vis_data.values() for vv in v.values())
    if args.type == 'line':
        build_line_plots(args, vis_data, max_val)
    elif args.type == 'violin':
        build_violin_plots(args, vis_data, max_val)
    elif args.type == 'both':
        build_violin_plots(args, vis_data, max_val)
        build_line_plots(args, vis_data, max_val)
    else:
        print("'%s' is not a valid plot type. Use 'python -m viewer --help' to see valid options." % args.type)


def main():
    args = parse_args()
    if args.path:
        files = get_files(args.path)
        full_data = get_full_data(args.path, files)  # indexed by monitoring level
        vis_data = get_visualization_data(full_data)  # indexed by micro name
        build_plots(args, vis_data)
    elif args.results:
        pass
    else:
        print('No results directory was specified.')


if __name__ == "__main__":
    main()
