if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')
import argparse
import sys
import html

from copy import copy
from functools import wraps

from tools.prov_parser import build_parser, prov
from tools.utils import unquote
from tools.view.style import default


def _quote(value):
    if value.startswith("<") and value.endswith(">"):
        return value
    if value.startswith('"') and value.endswith('"'):
        return value
    return '"{}"'.format(value)

class PrefixDict(dict):

    def __init__(self, prefixes, rprefixes):
        self.prefixes = prefixes
        self.rprefixes = rprefixes

    def __setitem__(self, item, value):
        if ":" in item:
            split = item.split(":", maxsplit=1)
            if split[0] not in self.prefixes:
                prefix = split[0]
                namespace = 'http://example.org/{}/'.format(prefix)
                self.prefixes[prefix] = namespace
                self.rprefixes[namespace] = prefix + ":"
        else:
            for v, p in self.rprefixes.items():
                if item.startswith(v):
                    item = item.replace(v, p, 1)
                    break
        super(PrefixDict, self).__setitem__(item, value)

    def generate_names(self, item):
        if isinstance(item, str):
            yield item

        item, *namespace = item
        for name in namespace:
            if name == "<any>":
                for iri, prefix in self.rprefixes.items():
                    yield prefix + item
                yield item
            if name in self.rprefixes:
                yield self.rprefixes[name] + item
            if name in self.prefixes:
                yield name + ":" + item

    def __getitem__(self, item):
        for qualified in self.generate_names(item):
            if qualified in self:
                return super(PrefixDict, self).__getitem__(qualified)


class Digraph(object):

    def __init__(self):
        self.functions = {"prefix": self.setprefix}
        self.attr = 0
        self.pointi = 0
        self.default_prefix = 'http://example.org/'
        self.prefixes = {
            "prov": "https://www.w3.org/ns/prov#"
        }
        self.rprefixes = {
            "https://www.w3.org/ns/prov#": "prov:"
        }
        self.rprefixes[self.default_prefix] = ""

        self.size_x = 16
        self.size_y = 12
        self.rankdir = "BT"
        self.header = ""
        self.footer = ""
        self.style = default

    def reset_config(self):
        self.size_x = 16
        self.size_y = 12
        self.rankdir = "BT"
        self.header = ""
        self.footer = ""
        self.style = default

    def reset(self):
        self.functions = {}
        self.reset_config()

    def generate(self, content):
        self.default_prefix = 'http://example.org/'
        self.prefixes = {
            "prov": "https://www.w3.org/ns/prov#"
        }
        self.rprefixes = {
            "https://www.w3.org/ns/prov#": "prov:"
        }
        self.rprefixes[self.default_prefix] = ""
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
            self.rprefixes[self.default_prefix] = ""
        else:
            old = (name, self.prefixes.get(name))
            self.prefixes[name] = iri
            self.rprefixes[iri] = name + ":"
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
                if "attrs" in kwargs:
                    attrs = kwargs["attrs"] or {}
                    new_attrs = PrefixDict(self.prefixes, self.rprefixes)
                    for key, value in attrs.items():
                        new_attrs[key] = unquote(value)
                    kwargs["attrs"] = new_attrs
                return fn(self, *args, **kwargs)
            self.functions[name] = func
            return func
        return dec

    def _node(self, name, attrs={}):
        """Create dot node"""
        extra = ""
        if attrs:
            extra = " [{}]".format(
                ",".join('{}={}'.format(key, _quote(value))
                         for key, value in attrs.items())
            )
        return '"{}"{}'.format(name, extra)

    def _arrow(self, *nodes, attrs={}, direction="->"):
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
        attrs = attrs or {}
        result = ""
        color = attrs.get("dot:hide", "gray")
        fontcolor = '<font color={}>{{}}</font>'.format(
            attrs["dot:hide"]
        ) if "dot:hide" in attrs else "{}"
        label = [
            '<<TABLE cellpadding="0" border="0">'
        ]
        added = False
        for key, value in attrs.items():
            if key.startswith("dot:"):
                continue
            added = True
            if key.startswith("prov:"):
                key = key[5:]
            label.append('\t<TR>')
            label.append('\t    <TD align="left">{}</TD>'.format(fontcolor.format(self.htmlescape(key) + ":")))
            label.append('\t    <TD align="left">{}</TD>'.format(fontcolor.format(self.htmlescape(unquote(value)))))
            label.append('\t</TR>')
        label.append('</TABLE>>')

        if added:
            aid = "-attrs{}".format(self.attr)
            self.attr += 1
            result = self._node(aid, {
                "color": color,
                "shape": "note",
                "fontsize": "10",
                "fontcolor": "black",
                "label": "\n".join(label)
            })
            if url is not None:
                result += "\n" + self._arrow(aid, url, attrs={
                    "color": color,
                    "style": "dashed",
                    "arrowhead": "none",
                })
        return result

    def node(self, attrs, statement, nid):
        url = self.prefix(nid)
        result = self._node(url, self.style.node(attrs, statement, nid, url))
        tattrs = self.attrs(attrs, url)
        if tattrs:
            result += "\n" + tattrs
        return result

    def arrow2(self, attrs, statement, first, second, label="", extra=""):
        if not first or not second:
            return None

        url1 = self.prefix(first)
        url2 = self.prefix(second)
        return self._arrow(url1, url2, attrs=self.style.arrow(attrs, statement, label, extra))

    def arrow3(self, attrs, statement, source, target1, target2, label0="", label1="", label2="", label3=""):
        if sum(1 for x in [source, target1, target2] if x) <= 1:
            return None

        if target1 and target2:
            point, result = self.point(attrs, statement)

            if source:
                surl = self.prefix(source)
                result += "\n" + self._arrow(surl, point, attrs=self.style.arrow(attrs, statement, label1, "1"))

            turl1 = self.prefix(target1)
            turl2 = self.prefix(target2)
            result += "\n" + self._arrow(point, turl1, attrs=self.style.arrow(attrs, statement, label0, "0"))
            result += "\n" + self._arrow(point, turl2, attrs=self.style.arrow(attrs, statement, label2, "2"))
            return result
        return self.arrow2(attrs, statement, source, target1 if target1 else target2, label3 or label0, extra="3")

    def point(self, attrs, statement):
        url = "bn{}".format(self.pointi)
        self.pointi += 1
        return url, self._node(url, self.style.point(attrs, statement))

    def replace(self, args, attrs):
        attrs = attrs or {}
        args = copy(args)
        for key, value in attrs.items():
            if key == "dot:hide":
                if "fillcolor" in args:
                    args["fillcolor"] = unquote(value)
            elif key == "dot:hide2":
                args["fontcolor"] = unquote(value)
                args["color"] = unquote(value)
            elif key.startswith("dot:"):
                args[key[4:]] = unquote(value)

        return args

    def escape(self, text):
        return text.replace('"', '\\"')

    def htmlescape(self, text):
        return html.escape(text)

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
