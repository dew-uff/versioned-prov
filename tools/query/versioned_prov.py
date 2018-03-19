"""Incomplete file with only the predicates we use in our mappings"""
if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.query.provn import *
from tools.utils import unquote, parsetime

@querier.prov("entity", ["id", "checkpoint", "text"])
def entity(querier, eid, attrs={}, id_=None):
    attrs = attrs or {}
    time = attrs.get("version:checkpoint")
    return [
        eid, parsetime(time),
        querier.text("entity", [eid], attrs, id_)
    ]


@querier.prov("wasDerivedFrom", ["generated", "used", "activity", "generation", "use", "type", "checkpoint", "whole", "key", "access", "attrs", "text"])
def wasDerivedFrom(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    attrs = attrs or {}
    return [
        eid1, eid2, aid, gid, uid,
        unquote(attrs.get("type")), parsetime(attrs.get("version:checkpoint")),
        unquote(attrs.get("version:whole")), unquote(attrs.get("version:key")), unquote(attrs.get("version:access")),
        attrs, querier.text("wasDerivedFrom", [eid1, eid2, aid, gid, uid], attrs, id_)
    ]

@querier.prov("wasGeneratedBy", ["id", "entity", "activity", "time", "checkpoint", "text"])
def wasGeneratedBy(dot, eid, aid=None, time=None, attrs=None, id_=None):
    attrs = attrs or {}
    return [
        id_, eid, aid, parsetime(time), parsetime(attrs.get("version:checkpoint")),
        querier.text("wasGeneratedBy", [eid, aid, time], attrs, id_)
    ]



@querier.prov("hadMember", ["collection", "entity", "type", "key", "checkpoint", "text"])
def hadMember(dot, ecollection=None, eid=None, attrs=None, id_=None):
    attrs = attrs or {}
    return [
        ecollection, eid,
        unquote(attrs.get("type")), unquote(attrs.get("version:key")), parsetime(attrs.get("version:checkpoint")),
        querier.text("hadMember", [ecollection, eid], attrs, id_)
    ]
