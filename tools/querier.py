# Copyright (c) 2017 Universidade Federal Fluminense (UFF)
# Copyright (c) 2017 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Pattern Matching Machinery"""
# pylint: disable=invalid-name
from collections import defaultdict, OrderedDict, Iterable
from functools import wraps

from prov_parser import build_parser, prov
from pattern_machinery import create_rule, var, BLANK, BoundQuery, Variable, NullQuery

class ProvQuery(BoundQuery):
    """Call rules function for all possibilities of unbound_options"""

    def __init__(self, name, nav, unbound_options):
        # pylint: disable=too-many-arguments
        super(ProvQuery, self).__init__()
        self.nav = nav
        self.name = name
        self.unbound_options = unbound_options

    def get_bound(self, result, attr):
        """Get bound value in result"""
        if attr in self.patterns:
            return self.patterns[attr].bound
        return BLANK

    def final_value(self, current):
        """Transform value"""
        # pylint: disable=no-self-use
        if current is BLANK:
            return var("_")
        if isinstance(current, Variable) and current.bound is not BLANK:
            return to_tuple(current.bound)
        return to_tuple(current)

    def prepare_values(self, bind):
        """Prepare values for exploration"""
        self.reset_patterns()
        new_values = []
        for arg, value, prevalue in bind:
            val = self.process_value(arg, prevalue)
            if val is not BLANK and val != value:
                # Variable bound to a different value
                return None
            elif val != value and isinstance(prevalue, Variable):
                prevalue.bound = value
                self.binds[prevalue] = value
            if value is not BLANK:
                new_values.append(value)
            else:
                new_values.append(prevalue)
        return map(self.final_value, new_values)

    def unfold(self, nav, order):
        if not nav:
            return []
        result = []

        (key, val), *rest = order
        values = nav[key]
        for value, subnav in values.items():
            sub = list(self.unfold(subnav, rest))
            if sub:
                for v in sub:
                    result.append([(key, value, val)] + v)
            else:
                result.append([(key, value, val)])
        return result

    def iterate(self):
        """generator"""
        for bind in self.unfold(self.nav, self.unbound_options):
            prep = self.prepare_values(bind)
            if prep is not None:
                yield self.name
            for pattern in self.binds:
                pattern.bound = BLANK


def to_tuple(data):
    if isinstance(data, str):
        return data
    if isinstance(data, Iterable):
        return tuple(to_tuple(x) for x in data)
    return data

class ProvRule(object):
    """Rule function"""
    # pylint: disable=too-few-public-methods

    def __init__(self, name, arguments):
        self.args = OrderedDict(
            (arg, i)
            for i, arg in enumerate(arguments)
        )
        self.arguments = arguments
        self.name = name
        self.nav = defaultdict(dict)
        self.__doc__ = "{}({})".format(name, ", ".join(self.args))

    def reset(self):
        self.nav = defaultdict(dict)

    def _add(self, pairs, nav):
        for i, (key, value) in enumerate(pairs):
            value = to_tuple(value)
            new_pairs = pairs[:i] + pairs[i + 1:]
            if not nav[key].get(value):
                nav[key][value] = defaultdict(dict)
            self._add(new_pairs, nav[key][value])

    def add(self, params):
        self._add(list(zip(self.arguments, params)), self.nav)

    def _process_val(self, val):
        """If bound value is ModelRule, returns its name"""
        return val

    def __call__(self, *args, **kwargs):
        values = [BLANK] * len(self.args)
        for i, val in enumerate(args):
            values[i] = self._process_val(val)
        for arg, val in kwargs.items():
            values[self.args[arg]] = self._process_val(val)

        unbound_options = []
        bound_options = []
        for arg, i in self.args.items():
            bound_value = values[i]
            if bound_value is BLANK or isinstance(bound_value, Variable):
                unbound_options.append((arg, bound_value))
            else:
                bound_options.append((arg, bound_value))
        nav = self.nav
        for arg, value in bound_options:
            if arg not in nav:
                return NullQuery()
            nav = nav[arg]
            value = to_tuple(value)
            if value not in nav:
                return NullQuery()
            nav = nav[value]
        return ProvQuery(self.name, nav, unbound_options)


class Querier(object):

    def __init__(self):
        self.functions = {"prefix": self.setprefix}
        self.rules = []
        #self.values = defaultdict(list)

    @prov("prefix")
    def setprefix(self, name, iri):
        return None

    def reset(self):
        self.functions = {}

    def generate(self, content):
        parser = build_parser(self.functions)
        return parser(content)

    def prov(self, name, arguments):
        def dec(fn):

            rule = ProvRule(name, arguments)

            @prov(name)
            @wraps(fn)
            def read(*args, **kwargs):
                result = fn(self, *args, **kwargs)
                #self.values[name].append(result)
                rule.add(result)
                return result

            self.functions[name] = read
            self.rules.append(rule)
            return rule
        return dec

    def text(self, name, args, attrs, id_):
        part1 = "" if id_ is None else "{}; ".format(id_)
        new_args = []
        for arg in args:
            if not arg:
                arg = "-"
            if isinstance(arg, (list, tuple)):
                arg = "{{{}}}".format(", ".join(
                    "({}, {})".format(key, value)
                    for key, value in arg
                ))
            new_args.append(arg)
        if attrs:
            text = "[{}]".format(
                ", ".join("{}={}".format(key, value)
                          for key, value in attrs.items())
            )
            new_args = new_args + [text]
        part2 = ", ".join(new_args)
        return "{}({}{})".format(name, part1, part2)

    def load(self, name):
        for rule in self.rules:
            rule.reset()
        with open(name, "r") as fil:
            return self.generate(fil.read())


querier = Querier()
