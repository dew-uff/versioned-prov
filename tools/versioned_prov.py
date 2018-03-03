from prov_dictionary import graph, _unquote, _dlabeldict, _darrow2


#referenceDerivedFrom(eid2, eid1, aid, gid, uid, timestamp) : wasDerivedFrom
@graph.prov("referenceDerivedFrom")
def reference_derived_from(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, time=None, attrs=None, id_=None):
    return _darrow2(dot, eid1, eid2, "der ref\n{}".format(time or "-"))


#usedPart(uid; aid, part_eid, key, whole_eid, timestamp) : used
@graph.prov("usedPart")
def used_part(dot, aid=None, eid=None, time=None, whole_eid=None, key=None, attrs=None, id_=None):
    return _darrow2(dot, aid, eid, "use\n{}[{}]\n{}".format(whole_eid or "-", _unquote(key) or "-", time or "-"))


#partGeneratedBy(eid, aid, timestamp, whole_eid, key) : wasGeneratedBy
@graph.prov("partGeneratedBy")
def part_generated_by(dot, eid, aid=None, time=None, whole_eid=None, key=None, attrs=None, id_=None):
    return _darrow2(dot, eid, aid, "gen\n{}[{}]\n{}".format(whole_eid or "-", _unquote(key) or "-", time or "-"))


#derivedByInsertion(vid2, {(ki, ei)...})
@graph.prov("derivedByInsertion")
def derived_by_insertion(dot, wid=None, changes=None, time=None, attrs=None, id_=None):
    result = []
    for pos, part in changes:
        if pos and pos.startswith('"') and pos.endswith('"'):
            pos = pos[1:-1]
        result.append(_darrow2(
            dot, wid, part, "der-ins\n[{}]\n{}".format(pos or "-", time or "-")
        ))
        #result.append(_darrow2(
        #    dot, part, eid, "der-ins-e\n[{}]\n{}".format(pos or "-", time or "-"),
        #    extra={"style":"dashed"}
        #))

    result = [x for x in result if x]
    if not result:
        return None
    return "\n".join(result)

