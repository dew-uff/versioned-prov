"""Incomplete file with only the predicates we use in our mappings"""
from qprov_dictionary import *

@querier.prov("entity", ["id", "time", "type", "text"])
def entity(querier, eid, attrs={}, id_=None):
    time = attrs.get("generatedAtTime")
    type_ = attrs.get("type")
    return [
        eid, parsetime(time), unquote(type_),
        querier.text("entity", [eid], attrs, id_)
    ]


@querier.prov("referenceDerivedFrom", ["generated", "used", "activity", "generation", "use", "time", "text"])
def reference_derived_from(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, time=None, attrs=None, id_=None):
    return [
        eid1, eid2, aid, gid, uid, parsetime(time),
        querier.text("referenceDerivedFrom", [eid1, eid2, aid, gid, uid, time], attrs, id_)
    ]


@querier.prov("referenceDerivedFromAccess", ["generated", "used", "activity", "generation", "use", "time", "whole", "key", "mode", "text"])
def reference_derived_from_access(dot, eid1=None, eid2=None, aid=None, gid=None, uid=None, time=None, whole=None, key=None, mode=None, attrs=None, id_=None):
    return [
        eid1, eid2, aid, gid, uid, parsetime(time), whole, key, mode,
        querier.text("referenceDerivedFromAccess", [eid1, eid2, aid, gid, uid, time, whole, key, mode], attrs, id_)
    ]
