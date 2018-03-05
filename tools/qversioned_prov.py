"""Incomplete file with only the predicates we use in our mappings"""
from qprovn import *
from utils import unquote, parsetime

@querier.prov("entity", ["id", "time", "text"])
def entity(querier, eid, attrs={}, id_=None):
    attrs = attrs or {}
    time = attrs.get("generatedAtTime")
    return [
        eid, parsetime(time),
        querier.text("entity", [eid], attrs, id_)
    ]


@querier.prov("wasDerivedFrom", ["generated", "used", "activity", "generation", "use", "type", "moment", "whole", "key", "mode", "text"])
def was_derived_from(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    attrs = attrs or {}
    return [
        eid1, eid2, aid, gid, uid,
        unquote(attrs.get("type")), parsetime(attrs.get("moment")),
        unquote(attrs.get("whole")), unquote(attrs.get("key")), unquote(attrs.get("access")),
        querier.text("wasDerivedFrom", [eid1, eid2, aid, gid, uid], attrs, id_)
    ]


@querier.prov("hadMember", ["collection", "entity", "type", "key", "moment", "text"])
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    attrs = attrs or {}
    return [
        ecollection, eid,
        unquote(attrs.get("type")), unquote(attrs.get("key")), parsetime(attrs.get("moment")),
        querier.text("hadMember", [ecollection, eid], attrs, id_)
    ]
