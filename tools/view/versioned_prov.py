if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.provn import graph, prov

NAMESPACE = "https://dew-uff.github.io/versioned-prov/ns#"

def versioned(attrs, key, default="-"):
    try:
        return attrs[(key, "version", "v", NAMESPACE)]
    except KeyError:
        return default

def ns_versioned(key):
    return {
        "version:" + key,
        NAMESPACE + key,
        key,
        "v:" + key,
    }


@graph.prov("hadMember")
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_versioned('Insertion'):
        return dot.arrow2(
            attrs, "ver_hadMember",
            ecollection, eid,
            "der-ins\n[{}]\n{}".format(
                versioned(attrs, 'key'),
                versioned(attrs, 'checkpoint'),
            ),
            extra="0"
        )
    if prov(attrs, 'type') in ns_versioned('Removal'):
        return dot.arrow2(
            attrs, "ver_hadMember",
            ecollection, eid,
            "der-rem\n[{}]\n{}".format(
                versioned(attrs, 'key'),
                versioned(attrs, 'checkpoint'),
            ),
            extra="1"
        )
    return dot.arrow2(attrs, "hadMember", ecollection, eid)


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    if aid and gid and uid:
        dot.used_required[(aid, eused)] = (uid, attrs)
        dot.generated_required[(egenerated, aid)] = (gid, attrs)
    if prov(attrs, 'type') in ns_versioned('Reference'):
        if versioned(attrs, 'access', False):
            return dot.arrow3(
                attrs, "ver_wasDerivedFrom",
                egenerated, versioned(attrs, 'whole'), eused,
                "",
                "der ac-{}\n{}".format(
                    versioned(attrs, 'access'),
                    versioned(attrs, 'checkpoint')
                ),
                "[{}]".format(versioned(attrs, 'key')),
            )
        return dot.arrow2(
            attrs, "ver_wasDerivedFrom",
            egenerated, eused, "der ref\n{}".format(
                versioned(attrs, 'checkpoint')
            ),
            extra="4"
        )
    checkpoint = versioned(attrs, 'checkpoint', False)
    if checkpoint:
        return dot.arrow2(attrs, "ver_wasDerivedFrom", egenerated, eused, "der\n{}".format(checkpoint), extra="5")
    return dot.arrow2(attrs, "wasDerivedFrom", egenerated, eused, "der")


@graph.prov("used")
def used(dot, aid, eid=None, time=None, attrs=None, id_=None):
    dot.used.add((aid, eid))
    checkpoint = versioned(attrs, 'checkpoint', False)
    if checkpoint:
        return dot.arrow2(attrs, "ver_used", aid, eid, "use\n{}".format(checkpoint))
    return dot.arrow2(attrs, "used", aid, eid, "use")

@graph.prov("wasGeneratedBy")
def was_generated_by(dot, aid, eid=None, time=None, attrs=None, id_=None):
    dot.used.add((aid, eid))
    checkpoint = versioned(attrs, 'checkpoint', False)
    if checkpoint:
        return dot.arrow2(attrs, "ver_wasGeneratedBy", aid, eid, "gen\n{}".format(checkpoint))
    return dot.arrow2(attrs, "wasGeneratedBy", aid, eid, "gen")