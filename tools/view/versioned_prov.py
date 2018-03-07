if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.provn import graph, prov
from tools.utils import unquote, garrow3, arrow2, garrow2

NAMESPACE = "https://dew-uff.github.io/versioned-prov/ns#"

def versioned(attrs, key, default="-"):
    try:
        return attrs[(key, "versioned", NAMESPACE)]
    except KeyError:
        return default

def ns_versioned(key):
    return {
        "versioned:" + key,
        NAMESPACE + key,
        key
    }

@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_versioned('Reference'):
        if versioned(attrs, 'access', False):
            return garrow3(
                dot, egenerated, versioned(attrs, 'whole'), eused,
                "[{}]".format(versioned(attrs, 'key')),
                extra={"label": "der ac-{}\n{}".format(
                    versioned(attrs, 'access'),
                    versioned(attrs, 'moment')
                )}, attrs=attrs
            )
        return garrow2(
            dot, egenerated, eused, "der ref\n{}".format(
                versioned(attrs, 'moment')
            ), attrs=attrs
        )
    return arrow2(dot, egenerated, eused, "der", attrs=attrs)


@graph.prov("hadMember")
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_versioned('Insertion'):
        return garrow2(
            dot, ecollection, eid, "der-ins\n[{}]\n{}".format(
                versioned(attrs, 'key'),
                versioned(attrs, 'moment'),
            ), attrs=attrs
        )
    if prov(attrs, 'type') in ns_versioned('Removal'):
        return garrow2(
            dot, ecollection, eid, "der-rem\n[{}]\n{}".format(
                versioned(attrs, 'key'),
                versioned(attrs, 'moment'),
            ), attrs=attrs
        )
    return arrow2(dot, ecollection, eid, "[ ]", attrs=attrs)
