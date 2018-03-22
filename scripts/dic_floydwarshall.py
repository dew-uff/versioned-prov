from pprint import pprint
import sys
sys.path.insert(0, '..')

import tools.view.prov_dictionary
import tools.annotations as prov

HIDE = prov.HIDE
SPECIFIC = prov.SPECIFIC

prov.reset_prov("../generated/prov_dictionary/")
prov.STATS_VIEW = 1

EMPTY = prov.entity("empty", "[]", "EmptyDictionary", None, None, attrs=SPECIFIC)

def empty(name):
    return EMPTY

def cond(ents):
    return ents

# Line 1
m = 10000 # max value
with prov.desc("L1 - assign", line=1) as line:
    e_n10000 = prov.entity("10000", "10000", prov.SCRIPT + "literal", None, line, attrs=HIDE)

    e_m = prov.entity("m", "10000", prov.SCRIPT + "name", "10000", line, attrs=HIDE)
    prov.activity("assign", [(e_m, e_n10000)], attrs=HIDE)

# Line 2
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    [2, m, 0]]
with prov.desc("L2 - list definition / assign", line=2) as line:
    with prov.desc("L2 - list definition"):
        e_n0 = prov.entity("0", "0", prov.SCRIPT + "literal", None, line + 1, attrs=HIDE)
        e_n1 = prov.entity("1", "1", prov.SCRIPT + "literal", None, line + 1, attrs=HIDE)
        e_n4 = prov.entity("4", "4", prov.SCRIPT + "literal", None, line + 1, attrs=HIDE)
        e_n2 = prov.entity("2", "2", prov.SCRIPT + "literal", None, line + 2, attrs=HIDE)

        prov_dist = [
            [e_n0, e_n1, e_n4],
            [e_m, e_n0, e_n2],
            [e_n2, e_m, e_n0]
        ]
        prov_label = [
            ["0", "1", "4"],
            ["m", "0", "2"],
            ["2", "m", "0"]
        ]
        e_list, rows = prov.define_array("matrix", dist, prov_label, line=line, show1=True, attrs=SPECIFIC)

        derived = []
        generated = [e_list]
        row_ents = []
        for i, row in enumerate(rows):
            generated.append(row[0])
            row_ents.append(row[0])
            prov.derivedByInsertionFrom(row[0], empty(row[0]), row[1], attrs=SPECIFIC)
            for j, ent in enumerate(row[1]):
                derived.append((ent, prov_dist[i][j]))
        prov.derivedByInsertionFrom(e_list, empty(e_list), row_ents, attrs=SPECIFIC)

        prov.activity("definelist", derived, generated=generated, attrs=SPECIFIC)

    with prov.desc("L2 - assign"):
        e_dist = prov.entity("dist", repr(dist), "Dictionary", "dist", line, show1=True)
        prov.derivedByInsertionFrom(e_dist, empty("dist"), row_ents, attrs=SPECIFIC)
        prov.activity("assign", [(e_dist, e_list)], attrs=HIDE)

        e_result = prov.entity("result", repr(result), "Dictionary", "result", line, show1=True)
        prov.derivedByInsertionFrom(e_result, empty("result"), row_ents, attrs=SPECIFIC)
        prov.activity("assign", [(e_result, e_list)], attrs=HIDE)

# Line 6
nodes = len(dist)
with prov.desc("L6 - func call / assign", line=6) as line:
    e_ret = prov.entity("len_dist", repr(nodes), prov.SCRIPT + "eval", "len(dist)", line, attrs=HIDE)
    prov.activity("call", [], [e_dist], [e_ret], label="len", attrs=HIDE)

    e_nodes = prov.entity("nodes", repr(nodes), prov.SCRIPT + "name", "nodes", line, attrs=HIDE)
    prov.activity("assign", [(e_nodes, e_ret)], attrs=HIDE)

# Line 7
indexes = range(nodes)
with prov.desc("L7 - func call / list assign", line=7) as line:
    e_ret = prov.entity("range_nodes", repr(list(indexes)), prov.SCRIPT + "eval", "range(nodes)", line)
    e_items = []
    for i in indexes:
        e_item = prov.entity("range_nodes{}".format(i), str(i), prov.SCRIPT + "item", None, line)
        e_items.append(e_item)

    prov.derivedByInsertionFrom(e_ret, empty("range_nodes"), e_items, attrs=SPECIFIC)
    prov.activity("call", [], [e_nodes], [e_ret] + e_items, label="range", attrs=HIDE)

    e_indexes = prov.entity("indexes", repr(list(indexes)), "Dictionary", "indexes", line)
    prov.derivedByInsertionFrom(e_indexes, empty("indexes"), e_items, attrs=SPECIFIC)

    prov.activity("assign", [(e_indexes, e_ret)], attrs=HIDE)

# Line 8
for k in indexes:
    with prov.desc("L8 - loop access", line=8) as line:
        e_k = prov.entity("k", k, prov.SCRIPT + "name", "k", line, show1=True, attrs=HIDE)
        prov.activity("access", [(e_k, prov.DICTS[e_indexes][repr(k)])], used=[e_indexes], attrs=HIDE)

    # Line 9
    distk = dist[k]
    with prov.desc("L9 - access / assign", line=9) as line:
        e_dist_ak = prov.entity("dist@k", repr(distk), "Dictionary", "dist[k]", line, show1=True)

        item = prov.DICTS[e_dist][str(k)]
        elements = [x[1] for x in sorted(list(prov.DICTS[item].items()))]
        prov.derivedByInsertionFrom(e_dist_ak, empty("dist_ak"), elements, attrs=SPECIFIC)
        prov.activity("access", [(e_dist_ak, item)], used=[e_dist, e_k], attrs=HIDE)

        e_distk = prov.entity("distk", repr(distk), "Dictionary", "distk", line, show1=True)
        prov.derivedByInsertionFrom(e_distk, empty("distk"), elements, attrs=SPECIFIC)
        prov.activity("assign", [(e_distk, e_dist_ak)], attrs=HIDE)

    # Line 10
    for i in indexes:
        with prov.desc("L10 - loop access", line=10) as line:
            e_i = prov.entity("i", i, prov.SCRIPT + "name", "i", line, show1=True, attrs=HIDE)
            prov.activity("access", [(e_i, prov.DICTS[e_indexes][repr(i)])], used=[e_indexes], attrs=HIDE)

        # Line 11
        with prov.desc("L11 - condition", line=11) as line:
            cond([e_i, e_k])
        if i == k: continue

        # Line 12
        disti = dist[i]
        with prov.desc("L12 - access / assign", line=12) as line:
            e_dist_ai = prov.entity("dist@i", repr(disti), "Dictionary", "dist[i]", line, show1=True)
            item = prov.DICTS[e_dist][str(i)]
            elements = [x[1] for x in sorted(list(prov.DICTS[item].items()))]
            prov.derivedByInsertionFrom(e_dist_ai, empty("dist_ai"), elements, attrs=SPECIFIC)
            prov.activity("access", [(e_dist_ai, item)], used=[e_dist, e_i], attrs=HIDE)

            e_disti = prov.entity("disti", repr(disti), "Dictionary", "disti", line, show1=True)
            prov.derivedByInsertionFrom(e_disti, empty("disti"), elements, attrs=SPECIFIC)
            prov.activity("assign", [(e_disti, e_dist_ai)], attrs=HIDE)

        # Line 13
        for j in indexes:
            with prov.desc("L13 - loop access", line=13) as line:
                e_j = prov.entity("j", j, prov.SCRIPT + "name", "j", line, show1=True, attrs=HIDE)
                prov.activity("access", [(e_j, prov.DICTS[e_indexes][repr(j)])], used=[e_indexes], attrs=HIDE)

            # Line 14
            with prov.desc("L14 - condition", line=14) as line:
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 15
            ikj = disti[k] + distk[j]
            with prov.desc("L15 - access / access / operation / assign", line=15) as line:
                e_disti_ak = prov.entity("disti@k", repr(disti[k]), prov.SCRIPT + "access", "disti[k]", line, show1=True, attrs=HIDE)
                item = prov.DICTS[e_disti][str(k)]
                prov.activity("access", [(e_disti_ak, item)], used=[e_disti, e_k], attrs=HIDE)

                e_distk_aj = prov.entity("distk@j", repr(distk[j]), prov.SCRIPT + "access", "distk[j]", line, show1=True, attrs=HIDE)
                item = prov.DICTS[e_distk][str(j)]
                prov.activity("access", [(e_distk_aj, item)], used=[e_distk, e_j], attrs=HIDE)

                e_sum = prov.entity("sum", repr(ikj), prov.SCRIPT + "operation", "disti[k] + distk[j]", line, show1=True, attrs=HIDE)
                prov.activity("+", [(e_sum, e_disti_ak, e_distk_aj)], attrs=HIDE)

                e_ikj = prov.entity("ikj", repr(ikj), prov.SCRIPT + "name", "ikj", line, show1=True, attrs=HIDE)
                prov.activity("assign", [(e_ikj, e_sum)], attrs=HIDE)

            # Line 16
            with prov.desc("L16 - access", line=16) as line:
                e_disti_aj = prov.entity("disti@j", repr(disti[j]), prov.SCRIPT + "access", "disti[j]", line, show1=True, attrs=HIDE)
                item = prov.DICTS[e_disti][str(j)]
                prov.activity("access", [(e_disti_aj, item)], used=[e_disti, e_j], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 17
                disti[j] = ikj

                with prov.desc("L17 - part assign with propagation", line=17) as line:
                    derived = []
                    used = [e_j]
                    used += ucond# from if
                    generated = []

                    e_disti_aj = prov.entity("disti@j", repr(ikj), prov.SCRIPT + "access", "disti[j]", line, show1=True)
                    derived.append((e_disti_aj, e_ikj))

                    new_e_disti = prov.entity("disti", repr(disti), "Dictionary", "disti", line, show1=True, attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(new_e_disti, e_disti, {j: e_disti_aj}, attrs=SPECIFIC)
                    derived.append(prov.Derivation((new_e_disti, e_disti, e_ikj), attrs=SPECIFIC))

                    new_e_distk = e_distk
                    if i == k:
                        new_e_distk = prov.entity("distk", repr(distk), "Dictionary", "distk", line, show1=True, attrs=SPECIFIC)
                        prov.derivedByInsertionFrom(new_e_distk, e_distk, {j: e_disti_aj}, attrs=SPECIFIC)
                        derived.append(prov.Derivation((new_e_distk, e_distk, e_ikj), attrs=SPECIFIC))

                    new_e_dist = prov.entity("dist", repr(dist), "Dictionary", "dist", line, show1=True, attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(new_e_dist, e_dist, {i: new_e_disti}, attrs=SPECIFIC)
                    derived.append(prov.Derivation((new_e_dist, e_dist, e_ikj), attrs=SPECIFIC))

                    new_e_result = prov.entity("result", repr(dist), "Dictionary", "result", line, show1=True, attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(new_e_result, e_result, {i: new_e_disti}, attrs=SPECIFIC)
                    derived.append(prov.Derivation((new_e_result, e_result, e_ikj), attrs=SPECIFIC))

                    prov.activity("assign", derived, used=used, generated=generated, shared=True)

                    e_disti = new_e_disti
                    e_distk = new_e_distk
                    e_dist = new_e_dist
                    e_result = new_e_result


# Line 18
print(result[0][2])
with prov.desc("L18 - access / access / call", line=18) as line:
    e_result_a0 = prov.entity("result@0", repr(result[0]), "Dictionary", "result[0]", line)
    item = prov.DICTS[e_result]["0"]
    elements = [x[1] for x in sorted(list(prov.DICTS[item].items()))]
    prov.derivedByInsertionFrom(e_result_a0, empty("result_a0"), elements, attrs=SPECIFIC)
    prov.activity("access", [(e_result_a0, item)], used=[e_result, e_n0], attrs=HIDE)

    e_result_a02 = prov.entity("result@0@2", repr(result[0][2]), prov.SCRIPT + "access", "result[0][2]", line, attrs=HIDE)
    item = prov.DICTS[e_result_a0]["2"]
    prov.activity("access", [(e_result_a02, item)], used=[e_result_a0, e_n2], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

prov.finish(show_count=False)
