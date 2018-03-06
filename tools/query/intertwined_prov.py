"""Incomplete file with only the predicates we use in our mappings"""
if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.query.prov_dictionary import *
from tools.utils import parsetime, unquote

@querier.prov("entity", ["id", "time", "type", "text"])
def entity(querier, eid, attrs={}, id_=None):
    attrs = attrs or {}
    time = attrs.get("generatedAtTime")
    type_ = attrs.get("type")
    return [
        eid, parsetime(time), unquote(type_),
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
