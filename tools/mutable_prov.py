from provn import graph

def _marrow2(dot, first, second, label="", extra={}):
    if not first or not second:
        return None

    url1 = dot.prefix(first)
    url2 = dot.prefix(second)

    labeldict = {
        "labelfontsize": "8",
        "labeldistance": "1.5",
        "color": "darkgreen",
        "labelangle": "60.0",
        "rotation": "20",
        "label": label
    }

    return dot.arrow(url1, url2, attrs=dict(**labeldict, **extra))

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
    return _marrow2(dot, eid, vid, "access\n{}".format(time or "-"))


@graph.prov("accessedPart")
def accessed_part(dot, eid=None, wid=None, key=None, pid=None, time=None, attrs=None, id_=None):
    if key and key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    return _marrow2(dot, eid, pid, "part\n{}[{}]\n{}".format(
        wid or "-", key or "-", time or "-"
    ))


@graph.prov("defined")
def defined(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    return _marrow2(dot, eid, vid, "defined\n{}".format(time or "-"), extra={"dir": "both"})


@graph.prov("derivedByInsertion")
def derived_by_insertion(dot, eid=None, wid=None, changes=None, time=None, attrs=None, id_=None):
    result = []
    for pos, part in changes:
        if pos and pos.startswith('"') and pos.endswith('"'):
            pos = pos[1:-1]
        result.append(_marrow2(
            dot, wid, part, "der-ins-v\n[{}]\n{}".format(pos or "-", time or "-")
        ))
        result.append(_marrow2(
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
        if pos and pos.startswith('"') and pos.endswith('"'):
            pos = pos[1:-1]
        result.append(_marrow2(
            dot, wid, eid, "der-rem\n[{}]\n{}".format(pos or "-", time or "-")
        ))

    result = [x for x in result if x]
    if not result:
        return None
    return "\n".join(result)


if __name__ == "__main__":
    graph.main()
