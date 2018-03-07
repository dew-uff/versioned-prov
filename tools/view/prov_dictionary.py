if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.provn import graph
from tools.utils import garrow2, garrow3, unquote, glabeldict
import tools.utils

@graph.prov("hadDictionaryMember")
def had_dictionary_member(dot, did=None, eid=None, key=None, attrs=None, id_=None):
    return garrow2(dot, did, eid, "[{}]".format(unquote(key)), attrs=attrs)


@graph.prov("derivedByInsertionFrom")
def derived_by_insertion_from(dot, dgen=None, duse=None, changes=None, attrs=None, id_=None):
    if not dgen:
        return None
    gen_url = dot.prefix(dgen)
    point, result = dot.point()
    result += "\n" + dot.arrow(gen_url, point, attrs=dot.replace({
        "arrowhead": "none",
        "taillabel": "der-ins",
        "color": tools.utils.HIGHLIGHT
    }, attrs))

    if duse:
        use_url = dot.prefix(duse)
        result += "\n" + dot.arrow(
            point, use_url, attrs=dot.replace(
                glabeldict("der"), attrs
            )
        )

    for key, ent in changes:
        key = unquote(key)
        if ent:
            ent_url = dot.prefix(ent)
            result += "\n" + dot.arrow(
                point, ent_url, attrs=dot.replace(
                    glabeldict("[{}]".format(key)), attrs
                )
            )
    return result


@graph.prov("derivedByRemovalFrom")
def derived_by_insertion_from(dot, dgen=None, duse=None, removals=None, attrs=None, id_=None):
    tremovals = ", ".join(
        "[{}]".format(unquote(x)) for x in removals if x
    )
    return garrow2(dot, dgen, duse, "der-rem\n{}".format(tremovals), attrs=attrs)

if __name__ == "__main__":
    graph.main()
