if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.prov_dictionary import graph
from tools.utils import unquote, garrow3, arrow2, garrow2

@graph.prov("entity")
def entity(dot, eid, attrs=None, id_=None):
    fillcolor = "#FFFC87"
    attrs = attrs or {}
    if attrs.get("type") == '"Version"':
        fillcolor = "#32CD32"

    url = dot.prefix(eid)
    result = dot.node(url, dot.replace({
        "fillcolor": fillcolor,
        "color": "#808080",
        "style": "filled",
        "label": eid,
        "URL": url,
    }, attrs))
    tattrs = dot.attrs(attrs, url)
    if tattrs:
        result += "\n" + tattrs
    return result


@graph.prov("wasDerivedFrom")
def was_derived_from(dot, egenerated=None, eused=None, aid=None, gid=None, uid=None, attrs=None, id_=None):
    attrs = attrs or {}
    if attrs.get('type') == '"Reference"':
        if 'access' in attrs:
            return garrow3(
                dot, egenerated, unquote(attrs.get("whole", "-")), eused,
                "[{}]".format(unquote(attrs.get("key", "-"))),
                extra={"label": "der ac-{}\n{}".format(
                    unquote(attrs.get("access", "-")),
                    unquote(attrs.get("moment", "-"))
                )}
            )
        return garrow2(
            dot, egenerated, eused, "der ref\n{}".format(unquote(attrs.get("moment", "-")))
        )
    return arrow2(dot, egenerated, eused, "der")

if __name__ == "__main__":
    graph.main()
