if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.provn import prov
from tools.view.prov_dictionary import graph
from tools.utils import unquote
import tools.utils

NAMESPACE = "https://dew-uff.github.io/versioned-prov/ns/intertwined#"

def intertwined(attrs, key, default="-"):
    try:
        return attrs[(key, "intertwined", NAMESPACE)]
    except KeyError:
        return default

def ns_intertwined(key):
    return {
        "intertwined:" + key,
        NAMESPACE + key,
        key
    }

@graph.prov("entity")
def entity(dot, eid, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_intertwined('Version'):
        return dot.node(attrs, "version", eid)
    return dot.node(attrs, "entity", eid)


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    if prov(attrs, 'type') in ns_intertwined('Reference'):
        if intertwined(attrs, 'access', False):
            return dot.arrow3(
                attrs, "int_wasDerivedFrom",
                egenerated, intertwined(attrs, 'whole'), eused,
                "[{}]".format(intertwined(attrs, 'key')),
                "der ac-{}\n{}".format(
                    intertwined(attrs, 'access'),
                    intertwined(attrs, 'moment')
                )
            )
        return dot.arrow2(
            attrs, "int_wasDerivedFrom",
            egenerated, eused, "der ref\n{}".format(
                intertwined(attrs, 'moment')
            ),
            extra="4"
        )
    return dot.arrow2(attrs, "wasDerivedFrom", egenerated, eused, "der")

if __name__ == "__main__":
    graph.main()
