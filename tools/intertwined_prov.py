from prov_dictionary import graph, _unquote, _dlabeldict, _darrow2, _darrow3


@graph.prov("entity")
def entity(dot, eid, attrs=None, id_=None):
    fillcolor = "#FFFC87"
    if attrs.get("type") == '"Version"':
        fillcolor = "#32CD32"

    url = dot.prefix(eid)
    result = dot.node(url, {
        "fillcolor": fillcolor,
        "color": "#808080",
        "style": "filled",
        "label": eid,
        "URL": url,
    })
    tattrs = dot.attrs(attrs, url)
    if tattrs:
        result += "\n" + tattrs
    return result


#referenceDerivedFrom(eid2, eid1, aid, gid, uid, timestamp) : wasDerivedFrom
@graph.prov("referenceDerivedFrom")
def reference_derived_from(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, time=None, attrs=None, id_=None):
    return _darrow2(dot, eid1, eid2, "der ref\n{}".format(time or "-"))


#referenceDerivedFromAccess(eid, pid, aid, gid, uid, timestamp, wid, key, mode) : wasDerivedFrom
@graph.prov("referenceDerivedFromAccess")
def reference_derived_from_access(dot, new=None, pid=None, aid=None, gid=None, uid=None, time=None, wid=None, key=None, mode=None, attrs=None, id_=None):
    return _darrow3(dot, new, wid, pid, "[{}]".format(_unquote(key) or "-"), extra={"label": "der ac-{}\n{}".format(_unquote(mode) or "-", time or "-")})

