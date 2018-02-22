"""Parser for PROV-N.

It does not comply completely with PROV-N.
It was designed to support only the situations we use in this repository in an extensible way.
"""

from collections import namedtuple

from lark import Lark, Transformer
from lark.lexer import Token


PARSER = Lark('''
    start: document

    document: "document" optional_declarations (expr)* (bundle)* "endDocument"

    ?optional_declarations: (namespace_declarations)?
    namespace_declarations: (default_namespace_declaration | namespace_declaration) (namespace_declaration)*
    namespace_declaration: "prefix" PN_PREFIX namespace
    default_namespace_declaration: "default" IRI_REF
    ?namespace: IRI_REF


    expr: QUALIFIED_NAME "(" optional_identifier arg ("," arg)* optional_attributes ")"

    optional_identifier: ( identifier_marker ";")?
    ?identifier_marker: identifier | "-"
    ?identifier: QUALIFIED_NAME

    arg: identifier_marker
       | literal
       | time
       | expr
       | tuple
    tuple: "{" arg ("," arg )* "}"
         | "(" arg ("," arg )* ")"


    ?optional_attributes: ( "," "[" attr_pairs "]")?
    attr_pairs: ( | attr_pair ("," attr_pair)* )
    attr_pair: attr "=" literal
    attr: QUALIFIED_NAME


    bundle: "bundle" identifier optional_declarations (expr)* "endBundle"

    ?literal: typed_literal
           | convenience_notation

    typed_literal: ESCAPED_STRING "%%" datatype
    ?datatype: QUALIFIED_NAME
    convenience_notation: ESCAPED_STRING (LANGTAG)?
                       | SIGNED_NUMBER
                       | QUALIFIED_NAME_LITERAL

    time: DATETIME

    DATETIME: (DIGIT DIGIT DIGIT DIGIT "-" DIGIT DIGIT "-" DIGIT DIGIT "T" DIGIT DIGIT ":" DIGIT DIGIT ":" DIGIT DIGIT ("." DIGIT DIGIT*)? ("Z" | TIMEZONE)?)
    TIMEZONE: ("+" | "-") DIGIT DIGIT ":" DIGIT DIGIT

    QUALIFIED_NAME: ( PN_PREFIX ":" )? PN_LOCAL
                  | PN_PREFIX ":"
    QUALIFIED_NAME_LITERAL: "'" QUALIFIED_NAME "'"
    LANGTAG: "@" LETTER+ ("-" (LETTER|DIGIT)+)*
    PN_PREFIX: PN_CHARS_BASE ((PN_CHARS | ".")* PN_CHARS)?
    PN_LOCAL: ( PN_CHARS_U | DIGIT ) ((PN_CHARS | ".")* PN_CHARS)?
    PN_CHARS_BASE: LETTER
                 | "\u00C0".."\u00D6"
                 | "\u00D8".."\u00F6"
                 | "\u00F8".."\u02FF"
                 | "\u0370".."\u037D"
                 | "\u037F".."\u1FFF"
                 | "\u200C".."\u200D"
                 | "\u2070".."\u218F"
                 | "\u2C00".."\u2FEF"
                 | "\u3001".."\uD7FF"
                 | "\uF900".."\uFDCF"
                 | "\uFDF0".."\uFFFD"
                 | "\U00010000".."\U000EFFFF"
    PN_CHARS: PN_CHARS_U
            | "-"
            | DIGIT
            | "\u00B7"
            | "\u0300".."\u036F"
            | "\u203F".."\u2040"
    PN_CHARS_U: PN_CHARS_BASE | "_"
    IRI_REF: "<" /.*/ ">"

    COMMENT: /\/\/[^\\n]*/

    %import common.CNAME
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.LETTER
    %import common.DIGIT
    %ignore COMMENT
    %ignore /[ \\t\\n\\f\\r]+/
''')


class CallProvN(Transformer):

    def __init__(self, functions={}):
        self.functions = functions

    def start(self, elements):
        return elements[0]

    def document(self, elements):
        if "document" in self.functions:
            return self.functions["document"](elements[0], elements[1:])
        else:
            return [x for x in elements if x is not None]

    def optional_declarations(self, elements):
        if elements:
            return elements
        return []

    def namespace_declarations(self, elements):
        if "<namespaces>" in self.functions:
            return self.functions["<namespaces>"](elements)
        else:
            filtered = [x for x in elements if x is not None]
            if filtered:
                return filtered
            return None

    def default_namespace_declaration(self, elements):
        params = ["<default>", elements[0].value]
        if "prefix" in self.functions:
            return self.functions["prefix"](*params)
        return self.functions["<warning>"]("prefix", *params)

    def namespace_declaration(self, elements):
        params = [x.value for x in elements]
        if "prefix" in self.functions:
            return self.functions["prefix"](*params)
        return self.functions["<warning>"]("prefix", *params)

    def expr(self, elements):
        name = elements[0]
        id_ = elements[1]
        attrs = elements[-1]
        params = elements[2:-1]
        if name.startswith("prov:"):
            name = name[5:]
        if name in self.functions:
            return self.functions[name](*params, id_=id_, attrs=attrs)
        return self.functions["<warning>"](name, *params, id_=id_, attrs=attrs)

    def arg(self, elements):
        element = elements[0]
        if isinstance(element, Token):
            return element.value
        if isinstance(element, str):
            return element
        if isinstance(element, list):
            return element

    def tuple(self, elements):
        return elements

    def optional_identifier(self, elements):
        if elements:
            return elements[0].value
        return None

    def identifier_marker(self, elements):
        if elements:
            print("AAAAAAAAAAAAA")
        return None

    def optional_attributes(self, elements):
        if elements:
            return elements
        return None

    def attr_pairs(self, elements):
        return {k:v for k, v in elements}

    def attr_pair(self, elements):
        return elements

    def attr(self, elements):
        return elements[0].value

    def typed_literal(self, elements):
        return Typed(*[x.value for x in elements])

    def convenience_notation(self, elements):
        return elements[0].value

    def bundle(self, elements):
        name, declarations, *expressions = elements
        name = name.value
        if "bundle" in self.functions:
            return self.functions["bundle"](name, declarations, expressions)
        return self.functions["<warning>"]("bundle", name, declarations, expressions)


def _warning(name, *args, id_=None, attrs=None):
    print("WARNING: '{}' is not defined!".format(name))


def provn_structure(content):
    """Surround contend with provn header and footer"""
    content = content.strip()
    if not content.startswith("document"):
        content = "document\ndefault <http://example.org/>\n" + content
    if not content.endswith("endDocument"):
        content = content + "\nendDocument"
    return content


def build_parser(functions, ignore_unnamed=False, warning=_warning):
    funcs = {
        "<warning>": warning,
    }
    if isinstance(functions, dict):
        for name, func in functions.items():
            if hasattr(func, 'provname'):
                funcs[func.provname] = func
            elif not ignore_unnamed:
                funcs[name] = func
    else:
        for func in functions.items():
            if hasattr(func, 'provname'):
                funcs[func.provname] = func
            elif not ignore_unnamed:
                funcs[func.__name__] = func

    transformer = CallProvN(funcs)
    def parser(content):
        tree = PARSER.parse(provn_structure(content))
        return transformer.transform(tree)
    return parser


def prov(name):
    def dec(fn):
        fn.provname = name
        return fn
    return dec
