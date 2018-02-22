import argparse
import sys

from functools import wraps

from prov_parser import build_parser, prov


def _quote(value):
    if value.startswith("<") and value.endswith(">"):
        return value
    if value.startswith('"') and value.endswith('"'):
        return value
    return '"{}"'.format(value)


def _unquote(value):
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


class Digraph(object):

    def __init__(self):
        self.functions = {"prefix": self.setprefix}
        self.attr = 0
        self.pointi = 0
        self.default_prefix = 'http://example.org/'
        self.prefixes = {}

        self.size_x = 16
        self.size_y = 12
        self.rankdir = "BT"
        self.header = ""
        self.footer = ""

    def reset_config(self):
        self.size_x = 16
        self.size_y = 12
        self.rankdir = "BT"
        self.header = ""
        self.footer = ""

    def reset(self):
        self.functions = {}
        self.reset_config()

    def generate(self, content):
        self.default_prefix = 'http://example.org/'
        self.prefixes = {}
        self.attr = 0
        self.pointi = 0
        parser = build_parser(self.functions)
        return parser(content)

    @prov("prefix")
    def setprefix(self, name, iri):
        iri = iri.strip()
        if iri.startswith("<"):
            iri = iri[1:]
        if iri.endswith(">"):
            iri = iri[:-1]
        if not iri.endswith("/"):
            iri += "/"
        if name == "<default>":
            old = ("<default>", self.default_prefix)
            self.default_prefix = iri
        else:
            old = (name, self.prefixes.get(name))
            self.prefixes[name] = iri
        return old

    def prefix(self, name):
        split = name.split(":")
        if len(split) == 1:
            prefix = self.default_prefix
        else:
            prefix = self.prefixes.get(split[0], self.default_prefix)
            name = ":".join(split[1:])
        return "{}{}".format(prefix, name)

    def prov(self, name):
        def dec(fn):
            @prov(name)
            @wraps(fn)
            def func(*args, **kwargs):
                return fn(self, *args, **kwargs)
            self.functions[name] = func
            return func
        return dec

    def node(self, name, attrs={}):
        """Create dot node"""
        extra = ""
        if attrs:
            extra = " [{}]".format(
                ",".join('{}={}'.format(key, _quote(value))
                         for key, value in attrs.items())
            )
        return '"{}"{}'.format(name, extra)

    def arrow(self, *nodes, attrs={}, direction="->"):
        """Create dot node"""
        extra = ""
        if attrs:
            extra = " [{}]".format(
                ",".join('{}={}'.format(key, _quote(value))
                         for key, value in attrs.items())
            )
        direction = " {} ".format(direction)
        return '{}{}'.format(direction.join(map(_quote, nodes)), extra)

    def attrs(self, attrs, url=None):
        """Create attrs node and associate it with a url"""
        result = ""
        if attrs:
            label = [
                '<<TABLE cellpadding="0" border="0">'
            ]
            for key, value in attrs.items():
                if key.startswith("prov:"):
                    key = key[5:]
                label.append('\t<TR>')
                label.append('\t    <TD align="left">{}:</TD>'.format(key))
                label.append('\t    <TD align="left">{}</TD>'.format(_unquote(value)))
                label.append('\t</TR>')
            label.append('</TABLE>>')

            aid = "-attrs{}".format(self.attr)
            self.attr += 1
            result = self.node(aid, {
                "color": "gray",
                "shape": "note",
                "fontsize": "10",
                "fontcolor": "black",
                "label": "\n".join(label)
            })
            if url is not None:
                result += "\n" + self.arrow(aid, url, attrs={
                    "color": "gray",
                    "style": "dashed",
                    "arrowhead": "none",
                })
        return result

    def point(self):
        url = "bn{}".format(self.pointi)
        self.pointi += 1
        return url, self.node(url, {
            "shape": "point",
            "label": "",
        })

    def main(self):
        parser = argparse.ArgumentParser(description='Convert PROV-N to GraphViz Dot')
        parser.add_argument('-i', '--infile', type=str, default=None,
                        help='Input PROV-N file')
        parser.add_argument('-o', '--outfile', type=str, default=None,
                        help='Output dot file')
        parser.add_argument('-x', '--width', type=int, default=16,
                        help='Graph width')
        parser.add_argument('-y', '--height', type=int, default=12,
                        help='Graph height')
        parser.add_argument('-r', '--rankdir', type=str, default="BT",
                        help='Graph rankdir')

        args = parser.parse_args([
            ("-" if x.startswith("-") and not x.startswith("--") and len(x) > 2 else "") + x
            for x in sys.argv[1:]
        ])

        if args.infile is None:
            provn = sys.stdin.read()
        else:
            with open(args.infile, "r") as f:
                provn = f.read()

        self.size_x = args.width
        self.size_y = args.height
        self.rankdir = args.rankdir
        result = self.generate(provn)
        if args.outfile is None:
            print(result)
        else:
            with open(args.outfile, "w") as f:
                f.write(result)

graph = Digraph()
