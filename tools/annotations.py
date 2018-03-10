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


class BaseOp:

    def fill(self, generated, used):
        pass

    def add(self, assign, gs, us, added, addunnamed=True):
        pass

class Use(BaseOp):

    def __init__(self, *values, attrs={}):
        self.used = {v: None for v in values}
        self.attrs = attrs

    def fill(self, generated, used):
        super(Use, self).fill(generated, used)
        for use, value in self.used.items():
            if use in used:
                if not value:
                    value = used.get(use)
                if not value:
                    value = get_varname("u", sep="", show1=True)
            used[use] = self.used[use] = value

    def add(self, assign, gs, us, added, addunnamed=True):
        super(Use, self).add(assign, gs, us, added, addunnamed=addunnamed)
        for use, value in self.used.items():
            value = us.get(use) or value
            if value and value not in added:
                add("used({}; {}, {}, -{})".format(value, assign, use, _attrpairs(self.attrs)))
                self.used[use] = value
                added.add(value)
            elif not value and addunnamed:
                add("used({}, {}, -{})".format(assign, use, _attrpairs(self.attrs)))

    def __repr__(self):
        return "U: " + ", ".join(x for x in self.used)

class Generation(BaseOp):

    def __init__(self, *values, attrs={}):
        self.generated = {v: None for v in values}
        self.attrs = attrs

    def fill(self, generated, used):
        super(Generation, self).fill(generated, used)
        for gen, value in self.generated.items():
            if gen in generated:
                if not value:
                    value = generated.get(gen)
                if not value:
                    value = get_varname("g", sep="", show1=True)
            generated[gen] = self.generated[gen] = value

    def add(self, assign, gs, us, added, addunnamed=True):
        super(Generation, self).add(assign, gs, us, added, addunnamed=addunnamed)
        for gen, value in self.generated.items():
            value = gs.get(gen) or value
            if value and value not in added:
                add("wasGeneratedBy({}; {}, {}, -{})".format(value, gen, assign, _attrpairs(self.attrs)))
                self.generated[gen] = value
                added.add(value)
            elif not value and addunnamed:
                add("wasGeneratedBy({}, {}, -{})".format(gen, assign, _attrpairs(self.attrs)))

    def __repr__(self):
        return "G: " + ", ".join(x for x in self.generated)

class Derivation(Use, Generation):

    def __init__(self, tup, attrs={}):
        gen, *use = tup
        Use.__init__(self, *use)
        Generation.__init__(self, gen)
        self.attrs = attrs

    def fill(self, generated, used):
        super(Derivation, self).fill(generated, used)
        for gen, varg in self.generated.items():
            if not varg and len(self.used) > 1:
                generated[gen] = self.generated[gen] = get_varname("g", sep="", show1=True)

    def add(self, assign, gs, us, added, addunnamed=False):
        for gen, varg in self.generated.items():
            if not varg:
                varg = gs[gen] = self.generated[gen] = get_varname("g", sep="", show1=True)
            added.add(varg)
            for use, varu in self.used.items():
                if not varu:
                    varu = us[use] = self.used[use] = get_varname("u", sep="", show1=True)
                added.add(varu)
                add("wasDerivedFrom({}, {}, {}, {}, {}{})".format(
                    gen, use, assign, varg, varu,
                    _attrpairs(self.derattrs(gen, use)))
                )

    def derattrs(self, gen, use):
        return self.attrs

    def __repr__(self):
        return "D({}, {})".format(Use.__repr__(self), Generation.__repr__(self))

class WriteDerivation(Derivation):

    def __init__(self, time, whole, key, gen, *use, attrs={}):
        self.time = time
        self.whole = whole
        self.key = key
        super(WriteDerivation, self).__init__(gen, *use, attrs=attrs)

    def derattrs(self, gen, use):
        SAME[gen] = SAME.get(use, use)
        return _buildattrs(self.attrs, [
            ("type", "Reference"),
            ("version:moment", self.time),
            ("version:whole", self.whole),
            ("version:key", self.key),
            ("version:access", "w"),
        ])

class AccessDerivation(Derivation):

    def __init__(self, time, whole, key, gen, *use, attrs={}):
        self.time = time
        self.whole = whole
        self.key = key
        super(WriteDerivation, self).__init__(gen, *use, attrs=attrs)

    def derattrs(self, gen, use):
        SAME[gen] = SAME.get(use, use)
        return _buildattrs(self.attrs, [
            ("type", "Reference"),
            ("version:moment", self.time),
            ("version:whole", self.whole),
            ("version:key", self.key),
            ("version:access", "r"),
        ])

class RefDerivation(Derivation):

    def __init__(self, time, gen, *use, attrs={}):
        self.time = time
        super(WriteDerivation, self).__init__(gen, *use, attrs=attrs)

    def derattrs(self, gen, use):
        SAME[gen] = SAME.get(use, use)
        return _buildattrs(self.attrs, [
            ("type", "Reference"),
            ("version:moment", self.time),
        ])

def clear_shared(gs, us, shared):
    if not shared:
        gs.clear()
        us.clear()


def instantiate(cls, elements, gs, us, shared, attrs, starred=False):
    clear_shared(gs, us, shared)
    new = []
    for element in elements:
        obj = element if isinstance(element, cls) else cls(element, attrs=attrs)
        obj.fill(gs, us)
        clear_shared(gs, us, shared)
        new.append(obj)
    return new

def activity(name, derived=[], used=[], generated=[], label=None, *, shared=False, attrs={}):
    varname = get_varname(name, sep="", show1=True)
    usages = {}
    new_attrs = _buildattrs(attrs, [
        ("type", name),
        ("label", label),
    ])
    add('activity({}{})'.format(varname, _attrpairs(new_attrs)))

    gs, us = {}, {}
    used = instantiate(Use, used, gs, us, shared, attrs)
    generated = instantiate(Generation, generated, gs, us, shared, attrs)
    derived = instantiate(Derivation, derived, gs, us, shared, attrs)

    added = set()
    for der in derived:
        der.add(varname, gs, us, added)
        clear_shared(gs, us, shared)

    for use in used:
        use.add(varname, gs, us, added)
        clear_shared(gs, us, shared)

    for gen in generated:
        gen.add(varname, gs, us, added)
        clear_shared(gs, us, shared)

    return varname

def value(name, value, *, attrs={}):
    varname = get_varname(name)
    new_attrs = _buildattrs(attrs, [
        ("repr", value),
    ])

    add('value({}{})'.format(varname, _attrpairs(new_attrs)))
    return varname

def defined(ent, value, time, attrs={}):
    add("defined({}, {}, {}{})".format(ent, value, time, _attrpairs(attrs)))
    add("wasDefinedBy({}, {}, {}{})".format(value, ent, time, _attrpairs(attrs)))
    VALUES[ent] = value

def accessed(ent, value, time, attrs={}):
    add("accessed({}, {}, {}{})".format(ent, value, time, _attrpairs(attrs)))
    VALUES[ent] = value

def accessedPart(ent, whole, key, part, time, attrs={}):
    add("accessedPart({}, {}, {}, {}, {}{})".format(ent, whole, key, part, time, _attrpairs(attrs)))
    VALUES[ent] = part

def derivedByInsertion(ent, whole, elements, time, attrs={}):
    if isinstance(elements, list):
        key_value = elements
    else:
        key_value = list(elements.items())

    add("derivedByInsertion({}, {}, {{{}}}, {}{})".format(
        ent, whole,
        ", ".join('("{}", {})'.format(i, v)
                  for i,v in key_value),
        time, _attrpairs(attrs)
    ))
    for i, v in key_value:
        DICTS[whole][str(i)] = v

def specializationOf(eid1, eid2, attrs={}):
    add('specializationOf({}, {}{})'.format(eid1, eid2, _attrpairs(attrs)))
    VALUES[eid1] = eid2

def hadMember(cname, entity, key, attrs={}):
    add("hadMember({}, {}{})".format(cname, entity, _attrpairs(attrs)))
    DICTS[cname][key] = entity

def vhadMember(cname, entity, key, time, attrs={}):
    new_attrs = _buildattrs(attrs, [
        ("type", "version:Insertion"),
        ("version:key", key),
        ("version:checkpoint", time),
    ])
    return hadMember(cname, entity, new_attrs)

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

def hadDictionaryMember(cid, eid, key, attrs):
    add("hadDictionaryMember({}, {}, {}{})".format(cid, eid, key, _attrpairs(attrs)))
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
