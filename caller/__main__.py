import argparse

from caller import micro, macro, macro_load


def parse_args():
    parser = argparse.ArgumentParser(description='Visualize micro results')
    parser.add_argument('--type', metavar='t', type=str, default='micro',
                        help='type of visualization. options: micro, macro, or both. default: micro')
    parser.add_argument('--load', metavar='l',  type=lambda x: (str(x).lower() in ['true', '1', 'yes', 'y']),
                        default=False, help='Generate load. options: true, false. default: false')
    args = parser.parse_args()
    return args


def run_benchmarks(args):
    if args.load:
        print("Generating load")
        macro_load.create_load()
        return
    if args.type == 'micro':
        micro.run()
    elif args.type == 'macro':
        macro.run()
    elif args.type == 'both':
        micro.run()
        macro.run()
    elif args.type == 'test_macro':
        macro.test()
    elif args.type == 'test_micro':
        micro.test()
    else:
        print("'%s' is not a valid benchmark type. Use 'python -m caller --help' to see valid options." % args.type)


def main():
    args = parse_args()
    run_benchmarks(args)


if __name__ == "__main__":
    main()
