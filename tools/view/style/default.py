from functools import partial
from tools.view.style.helpers import _apply, _join


HIGHLIGHT = "darkgreen"


def _label(label, attrs):
    if label:
        return {
            "labelfontsize": "8",
            "labeldistance": "1.5",
            "labelangle": "60.0",
            "rotation": "20",
            "taillabel": label
        }
    return {}


def _glabel(label, attrs):
    if label:
        return {
            "labelfontsize": "8",
            "labeldistance": "1.5",
            "color": HIGHLIGHT,
            "labelangle": "60.0",
            "rotation": "20",
            "label": label
        }
    return {"color": HIGHLIGHT}

def _after_node(statement, args, attrs):
    label, url = args
    return {
        "label": label,
        "URL": url,
    }

STYLE = {
    "node_after": _after_node,
    "label": _label,
    "point": {"shape": "point", "label": ""},

    "entity": {"fillcolor": "#FFFC87", "color": "#808080", "style": "filled"},
    "activity": {
        "fillcolor": "#9FB1FC", "color": "#0000FF",
        "shape": "polygon", "sides": "4", "style": "filled"
    },
    "agent": {"fillcolor": "#FDB266", "shape": "house", "style": "filled"},

    "wasStartedBy1": {"arrowhead": "none", "dir": "back", "arrowtail": "oinv"},
    "wasStartedBy3": {"dir": "back", "arrowtail": "oinv"},
    "wasEndedBy1": {"arrowhead": "none", "dir": "back", "arrowtail": "odiamond"},
    "wasEndedBy3": {"dir": "back", "arrowtail": "odiamond"},
    "wasInvalidatedBy": {"dir": "both", "arrowtail": "odiamond"},
    "wasAssociatedWith1": {"arrowhead": "none"},
    "actedOnBehalfOf1": {"arrowhead": "none"},
    "hadMember_label": lambda l, a: _label("[ ]", a),

    "derivedByInsertionFrom0_label*": _glabel,
    "derivedByInsertionFrom1": {"arrowhead": "none", "color": HIGHLIGHT},
    "derivedByInsertionFrom2_label*": _glabel,
    "hadDictionaryMember_label*": _glabel,

    "value": {"fillcolor": "#32CD32", "color": "#808080", "style": "filled"},
    "accessed_label*": _glabel,
    "accessedPart_label*": _glabel,
    "defined_label*": _glabel,
    "wasDefinedBy_label*": _glabel,
    "derivedByInsertion_label*": _glabel,
    "derivedByInsertion1": {"style":"dashed"},
    "derivedByRemoval_label*": _glabel,

    "version": {"fillcolor": "#32CD32", "color": "#808080", "style": "filled"},
    "int_wasDerivedFrom_label*": _glabel,
    "int_wasDerivedFrom1": {"arrowhead": "none"},


    "ver_hadMember_label*": _glabel,
    "ver_wasDerivedFrom_label*": _glabel,
    "ver_wasDerivedFrom1": {"arrowhead": "none"},
}


def arrow(attrs, statement, label="", extra=""):
    label_dict = {}
    _apply(STYLE, label_dict, "label", label, attrs)
    _apply(STYLE, label_dict, statement + "_label", label, attrs)
    if extra:
        _apply(STYLE, label_dict, statement + extra + "_label", label, attrs)

    arrow_dict = {}
    _apply(STYLE, arrow_dict, "arrow", attrs)
    _apply(STYLE, arrow_dict, statement, attrs)
    if extra:
        _apply(STYLE, arrow_dict, statement + extra, attrs)

    after_dict = {}
    _apply(STYLE, after_dict, "after", statement, (extra,), attrs)
    _apply(STYLE, after_dict, "arrow_after", statement, (extra,), attrs)

    return _join(label_dict, arrow_dict, after_dict)

def point(attrs, statement, extra=""):
    result = {}
    _apply(STYLE, result, "point", attrs)
    _apply(STYLE, result, statement + "_point", attrs)
    if extra:
        _apply(STYLE, result, statement + extra + "_point", attrs)

    after_dict = {}
    _apply(STYLE, after_dict, "after", statement, (extra,), attrs)
    _apply(STYLE, after_dict, "point_after", statement, (extra,), attrs)

    return _join(result, after_dict)


def node(attrs, statement, label="", url=""):
    label_dict = {}
    _apply(STYLE, label_dict, "node", label, url, attrs)
    _apply(STYLE, label_dict, statement, label, url, attrs)

    after_dict = {}
    _apply(STYLE, after_dict, "after", statement, (label, url), attrs)
    _apply(STYLE, after_dict, "node_after", statement, (label, url), attrs)
    return _join(label_dict, after_dict)

