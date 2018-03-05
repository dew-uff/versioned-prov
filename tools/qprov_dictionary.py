"""Incomplete file with only the predicates we use in our mappings"""
from qprovn import *


@querier.prov("derivedByInsertionFrom", ["generated", "used", "changes", "text"])
def derived_by_insertion_from(dot, dgen=None, duse=None, changes=None, attrs=None, id_=None):
    return [
        dgen, duse, changes,
        querier.text("derivedByInsertionFrom", [dgen, duse, changes], attrs, id_)
    ]

@querier.prov("hadDictionaryMember", ["dict", "entity", "key", "text"])
def had_dictionary_member(dot, did=None, eid=None, key=None, attrs=None, id_=None):
    return [
        did, eid, key,
        querier.text("hadDictionaryMember", [did, eid, key], attrs, id_)
    ]
