from provn import graph

def _dlabeldict(label):
    return {
        "labelfontsize": "8",
        "labeldistance": "1.5",
        "color": "darkgreen",
        "labelangle": "60.0",
        "rotation": "20",
        "label": label
    }


def _darrow2(dot, first, second, label="", extra={}):
    if not first or not second:
        return None

    url1 = dot.prefix(first)
    url2 = dot.prefix(second)

    return dot.arrow(url1, url2, attrs=dict(**_dlabeldict(label), **extra))


def _darrow3(dot, source, target1, target2, label, extra={}):
    if sum(1 for x in [source, target1, target2] if x) <= 1:
        return None

    if target1 and target2:
        point, result = dot.point()

        if source:
            surl = dot.prefix(source)
            result += "\n" + dot.arrow(surl, point, attrs=dict(**{
                "arrowhead": "none",
                "color": "darkgreen",
            }, **extra))

        turl1 = dot.prefix(target1)
        turl2 = dot.prefix(target2)
        result += "\n" + dot.arrow(point, turl1, attrs=_dlabeldict(label))
        result += "\n" + dot.arrow(point, turl2, attrs={"color": "darkgreen"})
        return result

    return _arrow2(dot, source, target1 if target1 else target2, label, extra)

def _unquote(key):
    if key and key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    return key

@graph.prov("hadDictionaryMember")
def had_dictionary_member(dot, did=None, eid=None, key=None, attrs=None, id_=None):
    if key and key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    return _darrow2(dot, did, eid, "[{}]".format(key))

@graph.prov("derivedByInsertionFrom")
def derived_by_insertion_from(dot, dgen=None, duse=None, changes=None, attrs=None, id_=None):
    if not dgen:
        return None
    gen_url = dot.prefix(dgen)
    point, result = dot.point()
    result += "\n" + dot.arrow(gen_url, point, attrs={
        "arrowhead": "none",
        "taillabel": "der-ins",
        "color": "darkgreen"
    })

    if duse:
        use_url = dot.prefix(duse)
        result += "\n" + dot.arrow(
            point, use_url, attrs=_dlabeldict("der")
        )

    for key, ent in changes:
        if key and key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        if ent:
            ent_url = dot.prefix(ent)
            result += "\n" + dot.arrow(
                point, ent_url, attrs=_dlabeldict("[{}]".format(key))
            )
    return result

@graph.prov("derivedByRemovalFrom")
def derived_by_insertion_from(dot, dgen=None, duse=None, removals=None, attrs=None, id_=None):
    tremovals = ", ".join(
        "[{}]".format(_unquote(x)) for x in removals if x
    )
    return _darrow2(dot, dgen, duse, "der-rem\n{}".format(tremovals))

if __name__ == "__main__":
    graph.main()
