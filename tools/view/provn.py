if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.dot import graph
from tools.utils import arrow2, arrow3


def prov(attrs, key, default="-"):
    if key in attrs:
        return attrs[key]
    try:
        return attrs[(key, "prov", "https://www.w3.org/ns/prov#")]
    except KeyError:
        return default


@graph.prov("document")
def documents(dot, declarations, elements):
    lines = [
        'digraph "PROV" {{ size="{},{}"; rankdir="{}";'.format(dot.size_x, dot.size_y, dot.rankdir)
    ]
    if dot.header:
        lines.append(dot.header)
    lines += [x for x in elements if x is not None]
    if dot.footer:
        lines.append(dot.footer)
    lines.append("}")
    return "\n".join(lines)


@graph.prov("entity")
def entity(dot, eid, attrs=None, id_=None):
    url = dot.prefix(eid)
    result = dot.node(url, dot.replace({
        "fillcolor": "#FFFC87",
        "color": "#808080",
        "style": "filled",
        "label": eid,
        "URL": url,
    }, attrs))
    tattrs = dot.attrs(attrs, url)
    if tattrs:
        result += "\n" + tattrs
    return result


@graph.prov("activity")
def activity(dot, aid, start_time=None, end_time=None, attrs=None, id_=None):
    url = dot.prefix(aid)
    result = dot.node(url, dot.replace({
        "fillcolor": "#9FB1FC",
        "color": "#0000FF",
        "shape": "polygon",
        "sides": "4",
        "style": "filled",
        "label": aid,
        "URL": url,
    }, attrs))
    tattrs = dot.attrs(attrs, url)
    if tattrs:
        result += "\n" + tattrs
    return result


@graph.prov("agent")
def agent(dot, agid, attrs=None, id_=None):
    url = dot.prefix(agid)
    result = dot.node(url, dot.replace({
        "fillcolor": "#FDB266",
        "shape": "house",
        "style": "filled",
        "label": agid,
        "URL": url,
    }, attrs))
    tattrs = dot.attrs(attrs, url)
    if tattrs:
        result += "\n" + tattrs
    return result


@graph.prov("wasGeneratedBy")
def was_generated_by(dot, eid, aid=None, time=None, attrs=None, id_=None):
    return arrow2(dot, eid, aid, "gen", attrs=attrs)


@graph.prov("used")
def used(dot, aid, eid=None, time=None, attrs=None, id_=None):
    return arrow2(dot, aid, eid, "use", attrs=attrs)


@graph.prov("wasInformedBy")
def was_informed_by(dot, informed, informant, attrs=None, id_=None):
    return arrow2(dot, informed, informant, "inf", attrs=attrs)


@graph.prov("wasStartedBy")
def was_started_by(dot, aid=None, etrigger=None, astarter=None, time=None, attrs=None, id_=None):
    return arrow3(dot, aid, etrigger, astarter, "start", extra={
        "dir": "back",
        "arrowtail": "oinv",
    }, attrs=attrs)


@graph.prov("wasEndedBy")
def was_ended_by(dot, aid=None, etrigger=None, aender=None, time=None, attrs=None, id_=None):
    return arrow3(dot, aid, etrigger, aender, "end", extra={
        "dir": "back",
        "arrowtail": "odiamond",
    }, attrs=attrs)


@graph.prov("wasInvalidatedBy")
def was_invalidated_by(dot, eid=None, aid=None, time=None, attrs=None, id_=None):
    return arrow2(dot, eid, aid, "inv", extra={
        "dir": "both",
        "arrowtail": "odiamond",
    }, attrs=attrs)


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    return arrow2(dot, egenerated, eused, "der", attrs=attrs)


@graph.prov("wasAttributedTo")
def was_attributed_to(dot, eid=None, agid=None, attrs=None, id_=None):
    return arrow2(dot, eid, agid, "att", attrs=attrs)


@graph.prov("wasAssociatedWith")
def was_associated_with(dot, aid=None, agid=None, eid=None, attrs=None, id_=None):
    return arrow3(dot, aid, agid, eid, "assoc", attrs=attrs)


@graph.prov("actedOnBehalfOf")
def acted_on_behalf_of(dot, agdelegate=None, agresponsible=None, eplan=None, attrs=None, id_=None):
    return arrow3(dot, agdelegate, agresponsible, eplan, "del", attrs=attrs)


@graph.prov("wasInfluencedBy")
def was_influenced_by(dot, einfluencee=None, einfluencer=None, attrs=None, id_=None):
    return arrow2(dot, einfluencee, einfluencer, "inf", attrs=attrs)


@graph.prov("alternateOf")
def alternate_of(dot, eid1=None, eid2=None, attrs=None, id_=None):
    return arrow2(dot, eid1, eid2, "alt", attrs=attrs)


@graph.prov("specializationOf")
def specialization_of(dot, especific=None, egeneral=None, attrs=None, id_=None):
    return arrow2(dot, especific, egeneral, "spe", attrs=attrs)


@graph.prov("hadMember")
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    return arrow2(dot, ecollection, eid, "[ ]", attrs=attrs)


@graph.prov("bundle")
def bundle(dot, name, declarations, elements):
    url = dot.prefix(name)
    lines = [
        'subgraph "cluster{}" {{'.format(url),
        '  label="{}";'.format(name),
        '  URL="{}";'.format(url)
    ]
    lines += [x for x in elements if x is not None]
    lines.append("}")
    for key, iri in declarations:
        if iri is not None:
            dot.setprefix(key, iri)
    return "\n".join(lines)


if __name__ == "__main__":
    graph.main()
