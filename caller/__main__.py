import argparse

from caller import micro, macro


def parse_args():
    parser = argparse.ArgumentParser(description='Visualize micro results')
    parser.add_argument('--type', metavar='t', type=str, default='micro',
                        help='type of visualization. options: micro, macro, or both. default: micro')
    args = parser.parse_args()
    return args


def run_benchmarks(args):
    if args.type == 'micro':
        micro.run()
    elif args.type == 'macro':
        macro.run()
    elif args.type == 'both':
        micro.run()
        macro.run()
    else:
        print("'%s' is not a valid benchmark type. Use 'python -m caller --help' to see valid options." % args.type)


def main():
    args = parse_args()
    run_benchmarks(args)


if __name__ == "__main__":
    main()
