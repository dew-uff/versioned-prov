"""Incomplete file with only the predicates we use in our mappings"""
from qprovn import *
from utils import parsetime


@querier.prov("value", ["id", "text"])
def value(dot, vid, attrs=None, id_=None):
    return [
        vid,
        querier.text("value", [vid], attrs, id_)
    ]


@querier.prov("accessed", ["entity", "value", "time", "text"])
def accessed(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, vid, ti,
        querier.text("accessed", [eid, vid, time], attrs, id_)
    ]


@querier.prov("accessedPart", ["entity", "whole", "key", "part", "time", "text"])
def accessed_part(dot, eid=None, wid=None, key=None, pid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, wid, key, pid, ti,
        querier.text("accessedPart", [eid, wid, key, pid, time], attrs, id_)
    ]


@querier.prov("defined", ["entity", "value", "time", "text"])
def defined(dot, eid=None, vid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, vid, ti,
        querier.text("defined", [eid, vid, time], attrs, id_)
    ]


@querier.prov("wasDefinedBy", ["value", "entity", "time", "text"])
def was_defined_by(dot, vid=None, eid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        vid, eid, ti,
        querier.text("wasDefinedBy", [vid, eid, time], attrs, id_)
    ]


@querier.prov("derivedByInsertion", ["entity", "whole", "changes", "time", "text"])
def derived_by_insertion(dot, eid=None, wid=None, changes=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        eid, wid, changes, ti,
        querier.text("derivedByInsertion", [eid, wid, changes, time], attrs, id_)
    ]
