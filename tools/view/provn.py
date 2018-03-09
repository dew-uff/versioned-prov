if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.dot import graph


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
    return dot.node(attrs, "entity", eid)


@graph.prov("activity")
def activity(dot, aid, start_time=None, end_time=None, attrs=None, id_=None):
    return dot.node(attrs, "activity", aid)


@graph.prov("agent")
def agent(dot, agid, attrs=None, id_=None):
    return dot.node(attrs, "agent", agid)


@graph.prov("wasGeneratedBy")
def was_generated_by(dot, eid, aid=None, time=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "wasGeneratedBy", eid, aid, "gen")


@graph.prov("used")
def used(dot, aid, eid=None, time=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "used", aid, eid, "use")


@graph.prov("wasInformedBy")
def was_informed_by(dot, informed, informant, attrs=None, id_=None):
    return dot.arrow2(attrs, "wasInformedBy", informed, informant, "inf")


@graph.prov("wasStartedBy")
def was_started_by(dot, aid=None, etrigger=None, astarter=None, time=None, attrs=None, id_=None):
    return dot.arrow3(attrs, "wasStartedBy", aid, etrigger, astarter, "start")


@graph.prov("wasEndedBy")
def was_ended_by(dot, aid=None, etrigger=None, aender=None, time=None, attrs=None, id_=None):
    return dot.arrow3(attrs, "wasEndedBy", aid, etrigger, aender, "end")


@graph.prov("wasInvalidatedBy")
def was_invalidated_by(dot, eid=None, aid=None, time=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "wasInvalidatedBy", eid, aid, "inv")


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    result = [dot.arrow2(attrs, "wasDerivedFrom", egenerated, eused, "der")]
    if not gid:
        result.append(was_generated_by(egenerated, aid, None, attrs))
    if not uid:
        result.append(used(aid, eused, None, attrs))
    return "\n".join(result)

@graph.prov("wasAttributedTo")
def was_attributed_to(dot, eid=None, agid=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "wasAttributedTo", eid, agid, "att")


@graph.prov("wasAssociatedWith")
def was_associated_with(dot, aid=None, agid=None, eid=None, attrs=None, id_=None):
    return dot.arrow3(attrs, "wasAssociatedWith", aid, agid, eid, "assoc")


@graph.prov("actedOnBehalfOf")
def acted_on_behalf_of(dot, agdelegate=None, agresponsible=None, eplan=None, attrs=None, id_=None):
    return dot.arrow3(attrs, "actedOnBehalfOf", agdelegate, agresponsible, eplan, "del")


@graph.prov("wasInfluencedBy")
def was_influenced_by(dot, einfluencee=None, einfluencer=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "wasInfluencedBy", einfluencee, einfluencer, "inf")


@graph.prov("alternateOf")
def alternate_of(dot, eid1=None, eid2=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "alternateOf", eid1, eid2, "alt")


@graph.prov("specializationOf")
def specialization_of(dot, especific=None, egeneral=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "specializationOf", especific, egeneral, "spe")


@graph.prov("hadMember")
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    return dot.arrow2(attrs, "hadMember", ecollection, eid)


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
