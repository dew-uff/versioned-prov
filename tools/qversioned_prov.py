"""Incomplete file with only the predicates we use in our mappings"""
from qprovn import *

@querier.prov("entity", ["id", "time", "text"])
def entity(querier, eid, attrs={}, id_=None):
    time = attrs.get("generatedAtTime")
    return [
        eid, parsetime(time),
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


@querier.prov("derivedByInsertion", ["entity", "changes", "time", "text"])
def derived_by_insertion(dot, wid=None, changes=None, time=None, attrs=None, id_=None):
    return [
        wid, changes, parsetime(time),
        querier.text("derivedByInsertion", [wid, changes, time], attrs, id_)
    ]
