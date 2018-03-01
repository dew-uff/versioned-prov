"""Incomplete file with only the predicates we use in our mappings"""
import dateutil.parser
from querier import querier, var, BLANK

def parsetime(time):
    if time and time.startswith("T"):
        return int(time[1:])
    try:
        return dateutil.parser.parse(time) if time else None
    except:
        return None


@querier.prov("entity", ["id", "text"])
def entity(querier, eid, attrs={}, id_=None):
    return [
        eid,
        querier.text("entity", [eid], attrs, id_)
    ]


@querier.prov("activity", ["id", "start", "end", "text"])
def activity(dot, aid, start_time=None, end_time=None, attrs=None, id_=None):
    start = parsetime(start_time)
    end = parsetime(end_time)
    return [
        aid, start, end,
        querier.text("activity", [aid, start_time, end_time], attrs, id_)
    ]


@querier.prov("used", ["id", "activity", "entity", "time", "text"])
def used(dot, aid, eid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        id_, aid, eid, ti,
        querier.text("used", [aid, eid, time], attrs, id_)
    ]


@querier.prov("wasDerivedFrom", ["generated", "used", "activity", "generation", "use", "text"])
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    return [
        egenerated, eused, aid, gid, uid,
        querier.text(
            "wasDerivedFrom",
            [egenerated, eused, aid, gid, uid], attrs, id_
        )
    ]


@querier.prov("wasGeneratedBy", ["id", "entity", "activity", "time", "text"])
def was_generated_by(dot, eid, aid=None, time=None, attrs=None, id_=None):
    ti = parsetime(time)
    return [
        id_, eid, aid, ti,
        querier.text("wasGeneratedBy", [eid, aid, time], attrs, id_)
    ]


@querier.prov("hadMember", ["collection", "entity", "text"])
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    return [
        ecollection, eid,
        querier.text("hadMember", [ecollection, eid], attrs, id_)
    ]




