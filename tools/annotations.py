from collections import Counter, defaultdict
from copy import copy
from contextlib import contextmanager

NAMES = Counter()
DICTS = defaultdict(dict)
ENABLED = True
RESULT = []
STATS = Counter()


def reset_prov():
    global DICTS
    global NAMES
    global ENABLED
    global RESULT
    global STATS
    DICTS = defaultdict(dict)
    NAMES = Counter()
    ENABLED = False
    RESULT = []
    STATS = Counter()


def add(text):
    STATS[text.split("(")[0]] += 1
    RESULT.append(text)
    if ENABLED:
        print(text)

def stats(path=None, view=False):
    provn = "\n".join(RESULT)
    if path:
        with open(path + ".provn", "w") as f:
            f.write(provn)
    if view is True:
        view = "png"
    if view:
        from IPython.display import display
        display(get_ipython().run_cell_magic(
            "provn",
            "-o {}.{}".format(path, view),
            provn
        ))
    return STATS.most_common()


def get_varname(name, num=None):
    if num is None:
        num = NAMES[name]
        NAMES[name] += 1
    return "{}{}".format(name, num)


def entity(name, value, type_, num=None, attrs={}):
    varname = get_varname(name, num)

    add('entity({}, [value="{}", type="{}"])'.format(varname, value, type_))
    return varname

def activity(name, derived=[], used=[], generated=[], num=None):
    varname = get_varname(name, num)
    add('activity({}, [type="{}"])'.format(varname, name))

    for new, *olds in derived:
        varg = get_varname("g")

        for old in olds:
            varu = get_varname("u")
            add("used({}; {}, {}, -)".format(varu, varname, old))
            add("wasDerivedFrom({}, {}, {}, {}, {})".format(new, old, varname, varg, varu))

        add("wasGeneratedBy({}; {}, {}, -)".format(varg, new, varname))


    for old in used:
        add("used({}, {}, -)".format(varname, old))

    for new in generated:
        add("wasGeneratedBy({}, {}, -)".format(new, varname))
    return varname

def hadMember(cname, entity, key):
    add("hadMember({}, {})".format(cname, entity))
    DICTS[cname][key] = entity

def hadDictionaryMember(dname, entity, key):
    add("hadDictionaryMember({}, {}, {})".format(dname, entity, key))
    DICTS[dname][key] = entity

def derivedByInsertionFrom(new, old, elements):
    if isinstance(elements, list):
        key_value = list(enumerate(elements))
    else:
        key_value = list(elements.items())

    add("derivedByInsertionFrom({}, {}, {{{}}})".format(
        new, old, ", ".join('("{}", {})'.format(i, v)
                           for i,v in key_value)
    ))
    DICTS[new] = copy(DICTS[old])
    for i, v in key_value:
        DICTS[new][repr(i)] = v

def nop(*args, **kwargs):
    pass

def define_array(name, value, type_="Dictionary", member=nop):
    varname = entity(name + "_", repr(value), type_)
    result = []
    for i, v in enumerate(value):
        iname = "{}{}".format(name, i)
        if isinstance(v, list):
            ref, _ = arr = define_array(iname, v, type_, member)
            result.append(arr)
        else:
            ref = entity(iname + "_", repr(v), "number")
            result.append(ref)
        member(varname, ref, repr(i))
    return varname, result

def derivation_pair(first, second, derivations=None):
    if derivations is None:
        derivations = []
    derivations.append((first, second))
    if first in DICTS:
        fd = DICTS[first]
        sd = DICTS[second]
        for key, fd_value in fd.items():
            sd_value = sd[key]
            derivation_pair(fd_value, sd_value, derivations)
    return derivations

def update(name, whole_ent, key, part_ent, whole_value):
    new_whole = entity(name, repr(whole_value), "list")
    key = repr(key)
    hadMember(new_whole, part_ent, key)
    for other_key, other_part in DICTS[whole_ent].items():
        hadMember(new_whole, other_part, other_key)
    return new_whole


@contextmanager
def desc(desc, enabled=False):
    global ENABLED
    if enabled:
        ENABLED = True
    yield
    if enabled:
        ENABLED = False
