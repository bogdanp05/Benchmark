import ast


def parse_string(parser, header, arg_name, arg_value):
    """
    Parse an argument from the given parser. If the argument is not specified, return the default value
    :param parser: the parser to be used for parsing
    :param header: name of the header in the configuration file
    :param arg_name: name in the configuration file
    :param arg_value: default value, if the value is not found
    """
    if parser.has_option(header, arg_name):
        return parser.get(header, arg_name)
    return arg_value


def parse_literal(parser, header, arg_name, arg_value):
    """
    Parse an argument from the given parser. If the argument is not specified, return the default value
    :param parser: the parser to be used for parsing
    :param header: name of the header in the configuration file
    :param arg_name: name in the configuration file
    :param arg_value: default value, if the value is not found
    """
    if parser.has_option(header, arg_name):
        return ast.literal_eval(parser.get(header, arg_name))
    return arg_value


def parse_list(parser, header, arg_name, arg_value):
    """
    Parse an argument from the given parser. If the argument is not specified, return the default value
    :param parser: the parser to be used for parsing
    :param header: name of the header in the configuration file
    :param arg_name: name in the configuration file
    :param arg_value: default value, if the value is not found
    """
    if parser.has_option(header, arg_name):
        val = ast.literal_eval(parser.get(header, arg_name))
        t = type(val)
        if t == list or t == tuple:
            return val
        if t == int:
            return [val]
    return arg_value


def parse_benchmarks(parser, header, default):
    """
    Parse an argument from the given parser. If the argument is not specified, return the default value
    :param parser: the parser to be used for parsing
    :param header: name of the header in the configuration file
    :param default: default value, the the value is not found
    """
    if parser.has_section(header):
        return parser.items(header)
    return default
