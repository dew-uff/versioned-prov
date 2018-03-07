if __name__ == "__main__":
    import sys; sys.path.insert(0, '../..')

from tools.view.provn import graph
from tools.utils import unquote, garrow3, arrow2, garrow2

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
                )}, attrs=attrs
            )
        return garrow2(
            dot, egenerated, eused, "der ref\n{}".format(unquote(attrs.get("moment", "-"))), attrs=attrs
        )
    return arrow2(dot, egenerated, eused, "der", attrs=attrs)


@graph.prov("hadMember")
def had_member(dot, ecollection=None, eid=None, attrs=None, id_=None):
    attrs = attrs or {}
    if attrs.get('type') == '"Insertion"':
        return garrow2(
            dot, ecollection, eid, "der-ins\n[{}]\n{}".format(
                unquote(attrs.get("key", "-")),
                unquote(attrs.get("moment", "-"))
            ), attrs=attrs
        )
    if attrs.get('type') == '"Removal"':
        return garrow2(
            dot, ecollection, eid, "der-rem\n[{}]\n{}".format(
                unquote(attrs.get("key", "-")),
                unquote(attrs.get("moment", "-"))
            ), attrs=attrs
        )
    return arrow2(dot, ecollection, eid, "[ ]", attrs=attrs)
