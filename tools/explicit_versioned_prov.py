from prov_dictionary import graph, _unquote, _dlabeldict, _darrow2


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


#hadVersion(eid, vid)
@graph.prov("hadVersion")
def had_version(dot, eid=None, vid=None, attrs=None, id_=None):
    return _darrow2(dot, eid, vid, "ver")


#referenceDerivedFrom(eid2, eid1, aid, gid, uid, timestamp) : derivedFrom, alternateOf?
@graph.prov("referenceDerivedFrom")
def derived_by_sharing_reference_from(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, time=None, attrs=None, id_=None):
    return _darrow2(dot, eid1, eid2, "der ref\n{}".format(time or "-"))


#hadItems(vid, {(ki, ei)...})
@graph.prov("hadItems")
def had_items(dot, vid=None, changes=None, attrs=None, id_=None):
    if not vid:
        return None
    gen_url = dot.prefix(vid)
    point, result = dot.point()
    result += "\n" + dot.arrow(gen_url, point, attrs={
        "arrowhead": "none",
        "taillabel": "had",
        "color": "darkgreen"
    })

    for key, ent in changes:
        if key and key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        if ent:
            ent_url = dot.prefix(ent)
            result += "\n" + dot.arrow(
                point, ent_url, attrs=_dlabeldict("[{}]".format(key))
            )
    return result


#usedPart(uid; aid, part_eid, key, whole_eid, timestamp) : used
@graph.prov("usedPart")
def used_part(dot, aid=None, eid=None, key=None, whole_eid=None, time=None, attrs=None, id_=None):
    return _darrow2(dot, aid, eid, "use\n{}[{}]\n{}".format(whole_eid or "-", _unquote(key) or "-", time or "-"))


#derivedByInsertionFrom(vid2, vid2, {(ki, ei)...})
