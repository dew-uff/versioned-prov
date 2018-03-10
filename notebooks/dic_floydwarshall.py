from pprint import pprint
import sys
sys.path.insert(0, '..')

import tools.view.prov_dictionary
import tools.annotations as prov

HIDE = prov.HIDE
SPECIFIC = prov.SPECIFIC

prov.reset_prov("../images/prov_dictionary/temp/")
prov.STATS_VIEW = 1

EMPTY = prov.entity("empty", "[]", "EmptyDictionary", None, attrs=SPECIFIC)

def empty(name):
    return EMPTY

def cond(ents):
    return ents

# Line 1
# Input graph

# Line 2
m = 10000 # max value
with prov.desc("L2 - assign", line=2):
    e_n10000 = prov.entity("10000", "10000", "literal", None, attrs=HIDE)

    e_m = prov.entity("m", "10000", "name", "10000", attrs=HIDE)
    prov.activity("assign", [(e_m, e_n10000)], attrs=HIDE)

# Line 3
lastrow = [2, m, 0]
with prov.desc("L3 - list definition / assign", line=3):
    with prov.desc("L3 - list definition"):
        e_n2 = prov.entity("2", "2", "literal", None, attrs=HIDE)
        e_n0 = prov.entity("0", "0", "literal", None, attrs=HIDE)

        prov_lastrow = [e_n2, e_m, e_n0]
        prov_label = ["2", "m", "0"]
        e_list, rows = prov.define_array("list", lastrow, prov_label, attrs=SPECIFIC)

        derived = []
        generated = [e_list]
        for i, ent in enumerate(rows):
            derived.append((ent, prov_lastrow[i]))
        prov.derivedByInsertionFrom(e_list, empty(e_list), rows, attrs=SPECIFIC)

        prov.activity("definelist", derived, generated=generated, attrs=SPECIFIC)

    with prov.desc("L3 - assign"):
        e_lastrow = prov.entity("lastrow", repr(lastrow), "Dictionary", "lastrow")
        prov.derivedByInsertionFrom(e_lastrow, empty(e_lastrow), rows, attrs=SPECIFIC)
        prov.activity("assign", [(e_lastrow, e_list)], attrs=HIDE)

# Line 4
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    lastrow
]
with prov.desc("L4 - list definition / assign", line=4):
    with prov.desc("L4 - list definition"):
        e_n1 = prov.entity("1", "1", "literal", None, attrs=HIDE)
        e_n4 = prov.entity("4", "4", "literal", None, attrs=HIDE)

        prov_dist = [
            [e_n0, e_n1, e_n4],
            [e_m, e_n0, e_n2],
            e_lastrow
        ]
        prov_label = [
            ["0", "1", "4"],
            ["m", "0", "2"],
            "lastrow"
        ]
        e_list, rows = prov.define_array("matrix", dist, prov_label, attrs=SPECIFIC)

        derived = []
        generated = [e_list]
        row_ents = []
        for i, row in enumerate(rows):
            if isinstance(row, tuple):
                generated.append(row[0])
                row_ents.append(row[0])
                prov.derivedByInsertionFrom(row[0], empty(row[0]), row[1], attrs=SPECIFIC)
                for j, ent in enumerate(row[1]):
                    derived.append((ent, prov_dist[i][j]))
            else:
                generated.append(row)
                prov.derivedByInsertionFrom(row, empty(row), prov.DICTS[e_lastrow], attrs=SPECIFIC)
                row_ents.append(row)
                derived.append((row, prov_dist[i]))
        prov.derivedByInsertionFrom(e_list, empty(e_list), row_ents, attrs=SPECIFIC)

        prov.activity("definelist", derived, generated=generated, attrs=SPECIFIC)

    with prov.desc("L4 - assign"):
        e_dist = prov.entity("dist", repr(dist), "Dictionary", "dist")
        prov.derivedByInsertionFrom(e_dist, empty("dist"), row_ents, attrs=SPECIFIC)
        prov.activity("assign", [(e_dist, e_list)], attrs=HIDE)

        e_result = prov.entity("result", repr(result), "Dictionary", "result")
        prov.derivedByInsertionFrom(e_result, empty("result"), row_ents, attrs=SPECIFIC)
        prov.activity("assign", [(e_result, e_list)], attrs=HIDE)

# Line 9
# Algorithm

# Line 10
nodes = len(dist)
with prov.desc("L10 - func call / assign", line=10):
    e_ret = prov.entity("len_dist", repr(nodes), "eval", "len(dist)", attrs=HIDE)
    prov.activity("call", [], [e_dist], [e_ret], label="len", attrs=HIDE)

    e_nodes = prov.entity("nodes", repr(nodes), "name", "nodes", attrs=HIDE)
    prov.activity("assign", [(e_nodes, e_ret)], attrs=HIDE)

# Line 11
indexes = range(nodes)
with prov.desc("L11 - func call / list assign", line=11):
    e_ret = prov.entity("range_nodes", repr(list(indexes)), "eval", "range(nodes)")
    e_items = []
    for i in indexes:
        e_item = prov.entity("range_nodes{}".format(i), str(i), "item", None)
        e_items.append(e_item)

    prov.derivedByInsertionFrom(e_ret, empty("range_nodes"), e_items, attrs=SPECIFIC)
    prov.activity("call", [], [e_nodes], [e_ret] + e_items, label="range", attrs=HIDE)

    e_indexes = prov.entity("indexes", repr(list(indexes)), "Dictionary", "indexes")
    prov.derivedByInsertionFrom(e_indexes, empty("indexes"), e_items, attrs=SPECIFIC)

    prov.activity("assign", [(e_indexes, e_ret)], attrs=HIDE)

# Line 12
for k in indexes:
    with prov.desc("L12 - loop access", line=12):
        e_k = prov.entity("k", k, "name", "k", attrs=HIDE)
        prov.activity("access", [(e_k, prov.DICTS[e_indexes][repr(k)])], used=[e_indexes], attrs=HIDE)

    # Line 13
    distk = dist[k]
    with prov.desc("L13 - access / assign", line=13):
        e_dist_ak = prov.entity("dist_ak", repr(distk), "Dictionary", "dist[k]")

        item = prov.DICTS[e_dist][str(k)]
        elements = [x[1] for x in sorted(list(prov.DICTS[item].items()))]
        prov.derivedByInsertionFrom(e_dist_ak, empty("dist_ak"), elements, attrs=SPECIFIC)
        prov.activity("access", [(e_dist_ak, item)], used=[e_dist, e_k], attrs=HIDE)

        e_distk = prov.entity("distk", repr(distk), "Dictionary", "distk")
        prov.derivedByInsertionFrom(e_distk, empty("distk"), elements, attrs=SPECIFIC)
        prov.activity("assign", [(e_distk, e_dist_ak)], attrs=HIDE)

    # Line 14
    for i in indexes:
        with prov.desc("L14 - loop access", line=14):
            e_i = prov.entity("i", i, "name", "i, attrs=HIDE")
            prov.activity("access", [(e_i, prov.DICTS[e_indexes][repr(i)])], used=[e_indexes], attrs=HIDE)

        # Line 15
        with prov.desc("L15 - condition", line=15):
            cond([e_i, e_k])
        if i == k: continue

        # Line 16
        disti = dist[i]
        with prov.desc("L16 - access / assign", line=16):
            e_dist_ai = prov.entity("dist_ai", repr(disti), "Dictionary", "dist[i]")
            item = prov.DICTS[e_dist][str(i)]
            elements = [x[1] for x in sorted(list(prov.DICTS[item].items()))]
            prov.derivedByInsertionFrom(e_dist_ai, empty("dist_ai"), elements, attrs=SPECIFIC)
            prov.activity("access", [(e_dist_ai, item)], used=[e_dist, e_i], attrs=HIDE)

            e_disti = prov.entity("disti", repr(disti), "Dictionary", "disti")
            prov.derivedByInsertionFrom(e_disti, empty("disti"), elements, attrs=SPECIFIC)
            prov.activity("assign", [(e_disti, e_dist_ai)], attrs=HIDE)

        # Line 17
        for j in indexes:
            with prov.desc("L17 - loop access", line=17):
                e_j = prov.entity("j", j, "name", "j", attrs=HIDE)
                prov.activity("access", [(e_j, prov.DICTS[e_indexes][repr(j)])], used=[e_indexes], attrs=HIDE)

            # Line 18
            with prov.desc("L18 - condition", line=18):
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 19
            ikj = disti[k] + distk[j]
            with prov.desc("L19 - access / access / operation / assign", line=19):
                e_disti_ak = prov.entity("disti_ak", repr(disti[k]), "access", "disti[k]", attrs=HIDE)
                item = prov.DICTS[e_disti][str(k)]
                prov.activity("access", [(e_disti_ak, item)], used=[e_disti, e_k], attrs=HIDE)

                e_distk_aj = prov.entity("distk_aj", repr(distk[j]), "access", "distk[j]", attrs=HIDE)
                item = prov.DICTS[e_distk][str(j)]
                prov.activity("access", [(e_distk_aj, item)], used=[e_distk, e_j], attrs=HIDE)

                e_sum = prov.entity("sum", repr(ikj), "operation", "disti[k] + distk[j]", attrs=HIDE)
                prov.activity("+", [(e_sum, e_disti_ak, e_distk_aj)], attrs=HIDE)

                e_ikj = prov.entity("ikj", repr(ikj), "name", "ikj", attrs=HIDE)
                prov.activity("assign", [(e_ikj, e_sum)], attrs=HIDE)

            # Line 20
            with prov.desc("L20 - access", line=20):
                e_disti_aj = prov.entity("disti_aj", repr(disti[j]), "access", "disti[j]", attrs=HIDE)
                item = prov.DICTS[e_disti][str(j)]
                prov.activity("access", [(e_disti_aj, item)], used=[e_disti, e_j], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 21
                disti[j] = ikj

                with prov.desc("L21 - part assign with propagation", line=21):
                    derived = []
                    used = [e_j]
                    used += ucond# from if
                    generated = []

                    e_disti_aj = prov.entity("disti_aj", repr(ikj), "access", "disti[j]")
                    derived.append((e_disti_aj, e_ikj))

                    new_e_disti = prov.entity("disti", repr(disti), "Dictionary", "disti", attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(new_e_disti, e_disti, {j: e_disti_aj}, attrs=SPECIFIC)
                    derived.append(prov.Derivation((new_e_disti, e_disti, e_ikj), attrs=SPECIFIC))

                    new_e_distk = e_distk
                    if i == k:
                        new_e_distk = prov.entity("distk", repr(distk), "Dictionary", "distk", attrs=SPECIFIC)
                        prov.derivedByInsertionFrom(new_e_distk, e_distk, {j: e_disti_aj}, attrs=SPECIFIC)
                        derived.append(prov.Derivation((new_e_distk, e_distk, e_ikj), attrs=SPECIFIC))

                    new_e_lastrow = e_lastrow
                    if i == nodes - 1:
                        new_e_lastrow = prov.entity("lastrow", repr(lastrow), "Dictionary", "lastrow", attrs=SPECIFIC)
                        prov.derivedByInsertionFrom(new_e_lastrow, e_lastrow, {j: e_disti_aj}, attrs=SPECIFIC)
                        derived.append(prov.Derivation((new_e_lastrow, e_lastrow, e_ikj), attrs=SPECIFIC))

                    new_e_dist = prov.entity("dist", repr(dist), "Dictionary", "dist", attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(new_e_dist, e_dist, {i: new_e_disti}, attrs=SPECIFIC)
                    derived.append(prov.Derivation((new_e_dist, e_dist, e_ikj), attrs=SPECIFIC))

                    new_e_result = prov.entity("result", repr(dist), "Dictionary", "result", attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(new_e_result, e_result, {i: new_e_disti}, attrs=SPECIFIC)
                    derived.append(prov.Derivation((new_e_result, e_result, e_ikj), attrs=SPECIFIC))

                    prov.activity("assign", [(e_disti_aj, e_ikj)], used=used, generated=generated, shared=True)

                    e_disti = new_e_disti
                    e_distk = new_e_distk
                    e_dist = new_e_dist
                    e_result = new_e_result
                    e_lastrow = new_e_lastrow


# Line 22
print(result[0][2])
with prov.desc("L22 - access / access / call", line=22):
    e_result_a0 = prov.entity("result_a0", repr(result[0]), "Dictionary", "result[0]")
    item = prov.DICTS[e_result]["0"]
    elements = [x[1] for x in sorted(list(prov.DICTS[item].items()))]
    prov.derivedByInsertionFrom(e_result_a0, empty("result_a0"), elements, attrs=SPECIFIC)
    prov.activity("access", [(e_result_a0, item)], used=[e_result, e_n0], attrs=HIDE)

    e_result_a02 = prov.entity("result_a02", repr(result[0][2]), "access", "result[0][2]", attrs=HIDE)
    item = prov.DICTS[e_result_a0]["2"]
    prov.activity("access", [(e_result_a02, item)], used=[e_result_a0, e_n2], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

pprint(prov.stats("../images/prov_dictionary/floydwarshall", True, engine="twopi"))