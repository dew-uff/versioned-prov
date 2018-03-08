from collections import OrderedDict

def _apply(style, result, name, *args):
    access = OrderedDict()
    if name in style:
        access = style[name]
    if name + "*" in style:
        access = style[name + "*"]
        result.clear()
    if callable(access):
        access = access(*args)
    for key, value in access.items():
        result[key] = value
    return result

def _join(new, *dicts):
    for dic in dicts:
        for key, value in dic.items():
            new[key] = value
    return new