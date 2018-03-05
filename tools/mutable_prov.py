from provn import graph
from utils import garrow2, unquote


@graph.prov("value")
def value(dot, vid, attrs=None, id_=None):
    url = dot.prefix(vid)
    result = dot.node(url, {
        "fillcolor": "#32CD32",
        "color": "#808080",
        "style": "filled",
        "label": vid,
        "URL": url,
    })
    tattrs = dot.attrs(attrs, url)
    if tattrs:
        result += "\n" + tattrs
    return result


@graph.prov("accessed")
def accessed(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    return garrow2(dot, eid, vid, "access\n{}".format(time or "-"))


@graph.prov("accessedPart")
def accessed_part(dot, eid=None, wid=None, key=None, pid=None, time=None, attrs=None, id_=None):
    key = unquote(key)
    return garrow2(dot, eid, pid, "part\n{}[{}]\n{}".format(
        wid or "-", key or "-", time or "-"
    ))


@graph.prov("defined")
def defined(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    return garrow2(dot, eid, vid, "defined\n{}".format(time or "-"))


@graph.prov("wasDefinedBy")
def was_defined_by(dot, vid=None, eid=None, time=None, attrs=None, id_=None):
    return garrow2(dot, vid, eid, "def by\n{}".format(time or "-"))


@graph.prov("derivedByInsertion")
def derived_by_insertion(dot, eid=None, wid=None, changes=None, time=None, attrs=None, id_=None):
    result = []
    for pos, part in changes:
        pos = unquote(pos)
        result.append(garrow2(
            dot, wid, part, "der-ins-v\n[{}]\n{}".format(pos or "-", time or "-")
        ))
        result.append(garrow2(
            dot, part, eid, "der-ins-e\n[{}]\n{}".format(pos or "-", time or "-"),
            extra={"style":"dashed"}
        ))

    result = [x for x in result if x]
    if not result:
        return None
    return "\n".join(result)


@graph.prov("derivedByRemoval")
def derived_by_removal(dot, eid=None, wid=None, positions=None, time=None, attrs=None, id_=None):
    result = []
    for pos in positions:
        pos = unquote(pos)
        result.append(garrow2(
            dot, wid, eid, "der-rem\n[{}]\n{}".format(pos or "-", time or "-")
        ))

    result = [x for x in result if x]
    if not result:
        return None
    return "\n".join(result)


if __name__ == "__main__":
    graph.main()
