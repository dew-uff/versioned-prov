if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.provn import graph, prov

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


@graph.prov("hadMember")
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_versioned('Insertion'):
        return dot.arrow2(
            attrs, "ver_hadMember",
            ecollection, eid,
            "der-ins\n[{}]\n{}".format(
                versioned(attrs, 'key'),
                versioned(attrs, 'moment'),
            ),
            extra="0"
        )
    if prov(attrs, 'type') in ns_versioned('Removal'):
        return dot.arrow2(
            attrs, "ver_hadMember",
            ecollection, eid,
            "der-rem\n[{}]\n{}".format(
                versioned(attrs, 'key'),
                versioned(attrs, 'moment'),
            ),
            extra="1"
        )
    return dot.arrow2(attrs, "hadMember", ecollection, eid)


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_versioned('Reference'):
        if versioned(attrs, 'access', False):
            return dot.arrow3(
                attrs, "ver_wasDerivedFrom",
                egenerated, versioned(attrs, 'whole'), eused,
                "[{}]".format(versioned(attrs, 'key')),
                "der ac-{}\n{}".format(
                    versioned(attrs, 'access'),
                    versioned(attrs, 'moment')
                )
            )
        return dot.arrow2(
            attrs, "ver_wasDerivedFrom",
            egenerated, eused, "der ref\n{}".format(
                versioned(attrs, 'moment')
            ),
            extra="4"
        )
    return dot.arrow2(attrs, "wasDerivedFrom", egenerated, eused, "der")
