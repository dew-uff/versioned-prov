from collections import Counter, defaultdict
from copy import copy
from contextlib import contextmanager
from os.path import join
import json

NAMES = Counter()
DICTS = defaultdict(dict)
ENABLED = True
RESULT = []
TEMP = []
STATS = defaultdict(Counter)
VALUES = {}
SAME = {}
TEMP_BASE = ""
LINE = None

def reset_prov(temp_base):
    global DICTS
    global NAMES
    global ENABLED
    global RESULT
    global STATS
    global VALUES
    global TEMP_BASE
    global SAME
    TEMP_BASE = temp_base
    DICTS = defaultdict(dict)
    NAMES = Counter()
    ENABLED = False
    RESULT = []
    TEMP = []
    STATS = defaultdict(Counter)
    VALUES = {}
    SAME = {}


def add(text):
    statement = text.split("(")[0]
    STATS["global"][statement] += 1
    STATS[LINE][statement] += 1
    RESULT.append(text)
    TEMP.append(text)
    if ENABLED:
        print(text)

def stats(path=None, view=False, temp=False, show=True):
    provn = "\n".join(TEMP if temp else RESULT)
    result = {}
    for key, stats in STATS.items():
        result[key] = stats.most_common()
    if path:
        with open(path + ".json", "w") as f:
            json.dump(result, f)
    if not view:
        view = "provn"
        show = False
    if view is True:
        view = "provn png svg pdf"
    from IPython.display import display
    im = get_ipython().run_cell_magic(
        "provn",
        "-o {} -e {}".format(path, view),
        provn
    )
    if show:
        display(im)
    return result


def get_varname(name, sep="#", show1=False):
    num = NAMES[name]
    NAMES[name] += 1
    num += 1
    extra = ""
    if num > 1 or show1:
        extra = "{}{}".format(sep, num)
    return "{}{}".format(name, extra)


def entity(name, value, type_, label, *, attrs={}):
    varname = get_varname(name)
    new_attrs = {}
    for key, value in [("value", value), ("type", type_), ("label", label)]:
        if value:
            new_attrs[key] = value
    for key, value in attrs.items():
        new_attrs[key] = value

    add('entity({}, [{}])'.format(varname, ",".join(
        '{}="{}"'.format(key, value)
        for key, value in new_attrs.items()
    )))
    return varname

def version(name, time):
    varname = get_varname(name + "_v", sep="", show1=True)
    add('entity({}, [generatedAtTime="{}", type="Version"])'.format(varname, time))
    return varname

def ventity(time, name, value, type_, label, *, attrs={}):
    new_attrs = {}
    new_attrs["generatedAtTime"] = time
    for key, value in attrs.items():
        new_attrs[key] = value
    return entity(name, value, type_, label, attrs=new_attrs)

def activity(name, derived=[], used=[], generated=[], label=None):
    varname = get_varname(name, sep="", show1=True)
    label = ', label="{}"'.format(label) if label else ""
    add('activity({}, [type="{}"{}])'.format(varname, name, label))

    for new, *olds in derived:
        varg = get_varname("g", sep="", show1=True)

        fnderived = lambda vn, vo, vu: add("wasDerivedFrom({}, {}, {}, {}, {})".format(vn, vo, varname, varg, vu))
        if new.startswith("--"):
            command = new[2:]
            if "g" in command:
                time, whole, key, new, *olds = olds
                def fnderived(vn, vo, vu):
                    add('wasDerivedFrom({}, {}, {}, {}, {}, [type="Reference", moment="{}", whole="{}", key="{}", access="w"])'.format(
                        vn, vo, varname, varg, vu, time, whole, key
                    ))
                    SAME[vn] = SAME.get(vo, vo)
            elif "p" in command:
                time, whole, key, new, *olds = olds
                def fnderived(vn, vo, vu):
                    add('wasDerivedFrom({}, {}, {}, {}, {}, [type="Reference", moment="{}", whole="{}", key="{}", access="r"])'.format(
                        vn, vo, varname, varg, vu, time, whole, key
                    ))
                    SAME[vn] = SAME.get(vo, vo)
            elif "d" in command:
                time, new, *olds = olds
                def fnderived(vn, vo, vu):
                    add('wasDerivedFrom({}, {}, {}, {}, {}, [type="Reference", moment="{}"])'.format(
                        vn, vo, varname, varg, vu, time
                    ))
                    SAME[vn] = SAME.get(vo, vo)

        for old in olds:
            varu = get_varname("u", sep="", show1=True)
            add("used({}; {}, {}, -)".format(varu, varname, old))
            fnderived(new, old, varu)

        add("wasGeneratedBy({}; {}, {}, -)".format(varg, new, varname))


    for old in used:
        add("used({}, {}, -)".format(varname, old))

    for new in generated:
        add("wasGeneratedBy({}, {}, -)".format(new, varname))
    return varname

def value(name, value, num=None, attrs={}):
    varname = get_varname(name)

    add('value({}, [repr="{}"])'.format(varname, value))
    return varname

def specializationOf(eid1, eid2):
    add('specializationOf({}, {})'.format(eid1, eid2))
    VALUES[eid1] = eid2


def defined(ent, value, time):
    add("defined({}, {}, {})".format(ent, value, time))
    add("wasDefinedBy({}, {}, {})".format(value, ent, time))
    VALUES[ent] = value

def accessed(ent, value, time):
    add("accessed({}, {}, {})".format(ent, value, time))
    VALUES[ent] = value

def accessedPart(ent, whole, key, part, time):
    add("accessedPart({}, {}, {}, {}, {})".format(ent, whole, key, part, time))
    VALUES[ent] = part

def derivedByInsertion(ent, whole, elements, time):
    if isinstance(elements, list):
        key_value = elements
    else:
        key_value = list(elements.items())

    add("derivedByInsertion({}, {}, {{{}}}, {})".format(
        ent, whole,
        ", ".join('("{}", {})'.format(i, v)
                  for i,v in key_value),
        time
    ))
    for i, v in key_value:
        DICTS[whole][str(i)] = v

def vderivedByInsertion(ent, elements, time):
    if isinstance(elements, list):
        key_value = elements
    else:
        key_value = list(elements.items())

    add("derivedByInsertion({}, {{{}}}, {})".format(
        ent,
        ", ".join('("{}", {})'.format(i, v)
                  for i,v in key_value),
        time
    ))
    for i, v in key_value:
        DICTS[ent][str(i)] = v


def hadMember(cname, entity, key):
    add("hadMember({}, {})".format(cname, entity))
    DICTS[cname][key] = entity

def vhadMember(cname, entity, key, time):
    add('hadMember({}, {}, [type="Insertion", key="{}", moment="{}"])'.format(
        cname, entity, key, time
    ))
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


def had_members(entity, elements):
    if isinstance(elements, list):
        key_value = list(enumerate(elements))
    else:
        key_value = list(elements.items())
    for i, v in key_value:
        hadMember(entity, v, str(i))

def nop(*args, **kwargs):
    pass


def calc_label(label):
    if isinstance(label, list):
        return "[{}]".format(", ".join(calc_label(x) for x in label))
    return label

def hadDictionaryMember(cid, eid, key):
    add("hadDictionaryMember({}, {}, {})".format(cid, eid, key))
    DICTS[cid][key] = eid

def define_array(name, value, label, type_="Dictionary", member=nop):
    varname = entity(name, repr(value), type_, calc_label(label))
    result = []
    for i, v in enumerate(value):
        iname = "{}{}".format(name, i)
        if isinstance(v, list):
            ref, _ = arr = define_array(iname, v, label[i], type_, member)
            result.append(arr)
        else:
            ref = entity(iname, repr(v), "item", label[i])
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

def update(name, whole_ent, key, part_ent, whole_value, label=None):
    new_whole = entity(name, repr(whole_value), "list", label)
    key = repr(key)
    for other_key, other_part in DICTS[whole_ent].items():
        if other_key != key:
            hadMember(new_whole, other_part, str(other_key))
    hadMember(new_whole, part_ent, str(key))
    return new_whole

@contextmanager
def desc(desc, enabled=False, line=None):
    global TEMP
    global LINE
    ltemp = LINE
    ptemp = TEMP
    TEMP = []
    if line is not None:
        LINE = line
    global ENABLED
    if enabled:
        ENABLED = True
    yield
    if enabled:
        ENABLED = False
    slug = (
        desc
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("[", "_")
        .replace("]", "_")
        .replace("__", "_")
    )

    stats(join(TEMP_BASE, get_varname(slug, sep="_")), "provn svg", True, False)
    TEMP = ptemp + TEMP
    LINE = ltemp
