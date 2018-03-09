if __name__ == "__main__":
    import sys; sys.path.insert(0, '..')

from collections import Counter, defaultdict
from copy import copy
from contextlib import contextmanager
from os.path import join
import json

from tools.prov_magics import ProvMagic

STATS_VIEW = True

NAMES = Counter()
DICTS = defaultdict(dict)
ENABLED = True
RESULT = []
TEMP = []
STATS = defaultdict(lambda: defaultdict(Counter))
VALUES = {}
SAME = {}
TEMP_BASE = ""
LINE = None

HIDE = {"dot:hide": "true"}
SPECIFIC = {"dot:specific": "true"}
BLACK = {"dot:color":"#000000"}

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
    STATS = defaultdict(lambda: defaultdict(Counter))
    VALUES = {}
    SAME = {}


def add(text):
    statement = text.split("(")[0]
    STATS["all"]["global"][statement] += 1
    STATS["all"][LINE][statement] += 1
    if not "dot:hide" in text:
        STATS["visible"]["global"][statement] += 1
        STATS["visible"][LINE][statement] += 1
    if "dot:specific" in text:
        STATS["specific"]["global"][statement] += 1
        STATS["specific"][LINE][statement] += 1

    RESULT.append(text)
    TEMP.append(text)
    if ENABLED:
        print(text)

def stats(path=None, view=False, temp=False, show=True, engine="dot"):
    provn = "\n".join(TEMP if temp else RESULT)
    if not provn:
        return
    result = {}
    for group, groups in STATS.items():
        result[group] = {}
        for key, stats in groups.items():
            result[group][key] = stats.most_common()
    if path:
        with open(path + ".json", "w") as f:
            json.dump(result, f)
    if not STATS_VIEW and not ENABLED:
        return result
    if not view:
        view = "provn"
        show = False
    if view is True:
        view = "provn png svg pdf"
    from IPython.display import display
    if engine != "dot":
        provn = 'graph [overlap=false]\n##H##\n' + provn
    im = ProvMagic().provn("-o {} -e {} -p {} -s hide".format(path, view, engine), provn)
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

def _attrpairs(new_attrs):
    if not new_attrs:
        return ""
    return ", [{}]".format(",".join(
        '{}="{}"'.format(key, value)
        for key, value in new_attrs.items()
    ))

def _buildattrs(attrs, pairs):
    pairs = pairs or []
    attrs = attrs or {}
    new_attrs = {}
    for key, value in pairs:
        if value:
            new_attrs[key] = value
    for key, value in attrs.items():
        new_attrs[key] = value
    return new_attrs


def entity(name, value, type_, label, *, attrs={}):
    varname = get_varname(name)
    new_attrs = _buildattrs(attrs, [
        ("value", value),
        ("type", type_),
        ("label", label)
    ])
    add('entity({}{})'.format(varname, _attrpairs(new_attrs)))
    return varname

def version(name, time, *, attrs={}):
    varname = get_varname(name + "_v", sep="", show1=True)
    new_attrs = _buildattrs(attrs, [
        ("generatedAtTime", time),
        ("type", "Version"),
    ])
    add('entity({}{})'.format(varname, _attrpairs(new_attrs)))
    return varname

def ventity(time, name, value, type_, label, *, attrs={}):
    new_attrs = _buildattrs(attrs, [
        ("generatedAtTime", time),
    ])
    return entity(name, value, type_, label, attrs=new_attrs)

def activity(name, derived=[], used=[], generated=[], label=None, *, shared=False, attrs={}):
    varname = get_varname(name, sep="", show1=True)
    usages = {}
    new_attrs = {}
    wdf_attrs = {}
    wgb_attrs = {}
    u_attrs = {}
    mod = {}
    for key, value in attrs.items():
        if key.startswith("wasDerivedFrom:"):
            wdf_attrs[key[15:]] = value
        elif key.startswith("wasGeneratedBy:"):
            wgb_attrs[key[15:]] = value
        elif key.startswith("used:"):
            u_attrs[key[5:]] = value
        elif key.startswith("attrs:"):
            key = key[6:]
            wdf_attrs[key] = wgb_attrs[key] = u_attrs[key] = value
        elif key.startswith("dot:"):
            new_attrs[key] = wdf_attrs[key] = wgb_attrs[key] = u_attrs[key] = value
        else:
            new_attrs[key] = value

    new_attrs = _buildattrs(new_attrs, [
        ("type", name),
        ("label", label),
    ])
    add('activity({}{})'.format(varname, _attrpairs(new_attrs)))

    for new, *olds in derived:
        varg = get_varname("g", sep="", show1=True)

        fnderived = lambda vn, vo, vu: wdf_attrs
        if new.startswith("--"):
            command = new[2:]
            new, *olds = olds
            if "s" in command:
                mod = SPECIFIC
                for key, value in mod.items():
                    u_attrs[key] = value
                    wdf_attrs[key] = value
                    wgb_attrs[key] = value
            if "g" in command:
                time = new
                whole, key, new, *olds = olds
                def fnderived(vn, vo, vu):
                    SAME[vn] = SAME.get(vo, vo)
                    attrs = copy(wdf_attrs)
                    attrs["type"] = "Reference"
                    attrs["moment"] = time
                    attrs["whole"] = whole
                    attrs["key"] = key
                    attrs["access"] = "w"
                    return attrs
            elif "p" in command:
                time = new
                whole, key, new, *olds = olds
                def fnderived(vn, vo, vu):
                    SAME[vn] = SAME.get(vo, vo)
                    attrs = copy(wdf_attrs)
                    attrs["type"] = "Reference"
                    attrs["moment"] = time
                    attrs["whole"] = whole
                    attrs["key"] = key
                    attrs["access"] = "r"
                    return attrs
            elif "d" in command:
                time = new
                new, *olds = olds
                def fnderived(vn, vo, vu):
                    SAME[vn] = SAME.get(vo, vo)
                    attrs = copy(wdf_attrs)
                    attrs["type"] = "Reference"
                    attrs["moment"] = time
                    return attrs

        for old in olds:
            if shared and old in usages:
                varu = usages[old]
            else:
                varu = get_varname("u", sep="", show1=True)
                add("used({}; {}, {}, -{})".format(varu, varname, old, _attrpairs(u_attrs)))
                usages[old] = varu
            add("wasDerivedFrom({}, {}, {}, {}, {}{})".format(new, old, varname, varg, varu, _attrpairs(fnderived(new, old, varu))))
        add("wasGeneratedBy({}; {}, {}, -{})".format(varg, new, varname, _attrpairs(wgb_attrs)))

        if mod:
            for key in mod:
                del u_attrs[key]
                del wdf_attrs[key]
                del wgb_attrs[key]


    for old in used:
        if shared and old in usages:
            varu = usages[old]
        else:
            varu = get_varname("u", sep="", show1=True)
            add("used({}; {}, {}, -{})".format(varu, varname, old, _attrpairs(u_attrs)))
            usages[old] = varu

    for new in generated:
        add("wasGeneratedBy({}, {}, -{})".format(new, varname, _attrpairs(wgb_attrs)))
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


def hadMember(cname, entity, key, attrs={}):
    add("hadMember({}, {}{})".format(cname, entity, _attrpairs(attrs)))
    DICTS[cname][key] = entity

def vhadMember(cname, entity, key, time):
    add('hadMember({}, {}, [type="Insertion", key="{}", moment="{}"])'.format(
        cname, entity, key, time
    ))
    DICTS[cname][key] = entity


def hadDictionaryMember(dname, entity, key, *, attrs=BLACK):
    add("hadDictionaryMember({}, {}, {}{})".format(
        dname, entity, key, _attrpairs(attrs)
    ))
    DICTS[dname][key] = entity

def derivedByInsertionFrom(new, old, elements, *, attrs=BLACK):
    if isinstance(elements, list):
        key_value = list(enumerate(elements))
    else:
        key_value = list(elements.items())

    add("derivedByInsertionFrom({}, {}, {{{}}}{})".format(
        new, old, ", ".join('("{}", {})'.format(i, v)
                            for i,v in key_value),
        _attrpairs(attrs)
    ))
    DICTS[new] = copy(DICTS[old])
    for i, v in key_value:
        DICTS[new][repr(i)] = v


def had_members(entity, elements, attrs={}):
    if isinstance(elements, list):
        key_value = list(enumerate(elements))
    else:
        key_value = list(elements.items())
    for i, v in key_value:
        hadMember(entity, v, str(i), attrs=attrs)

def nop(*args, **kwargs):
    pass


def calc_label(label):
    if isinstance(label, list):
        return "[{}]".format(", ".join(calc_label(x) for x in label))
    return label

def hadDictionaryMember(cid, eid, key):
    add("hadDictionaryMember({}, {}, {})".format(cid, eid, key))
    DICTS[cid][key] = eid

def define_array(name, value, label, type_="Dictionary", member=nop, attrs={}, first_attrs={}):
    varname = entity(name, repr(value), type_, calc_label(label), attrs=first_attrs)
    result = []
    for i, (v, l) in enumerate(zip(value, label)):
        iname = "{}{}".format(name, i)
        if isinstance(l, list):
            ref, _ = arr = define_array(iname, v, l, type_, member, attrs=attrs, first_attrs=first_attrs)
            result.append(arr)
        else:
            ref = entity(iname, repr(v), "item", l, attrs=attrs)
            result.append(ref)
        member(varname, ref, repr(i), attrs=attrs)
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

def update(name, whole_ent, key, part_ent, whole_value, label=None, attrs={}):
    new_whole = entity(name, repr(whole_value), "list", label, attrs=attrs)
    key = repr(key)
    for other_key, other_part in DICTS[whole_ent].items():
        if other_key != key:
            hadMember(new_whole, other_part, str(other_key), attrs=attrs)
    hadMember(new_whole, part_ent, str(key), attrs=attrs)
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
    if enabled:
        ENABLED = False
