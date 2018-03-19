from datetime import datetime
from pprint import pprint
import sys
sys.path.insert(0, '..')

import tools.view.mutable_prov
import tools.annotations as prov

HIDE = prov.HIDE
SPECIFIC = prov.SPECIFIC

prov.reset_prov("../generated/mutable_prov/")
prov.STATS_VIEW = 1

def time():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

def cond(ents):
    return ents

# Line 1
# Input graph

# Line 2
m = 10000 # max value
with prov.desc("L2 - assign", line=2):
    e_n10000 = prov.entity("10000", None, "literal", "10000", attrs=HIDE)
    v_10000 = prov.value("v10000", "10000", attrs=SPECIFIC)
    prov.defined(e_n10000, v_10000, time(), attrs=SPECIFIC)

    e_m = prov.entity("m", None, "name", "m", attrs=HIDE)
    prov.activity("assign", [(e_m, e_n10000)], attrs=HIDE)
    prov.accessed(e_m, v_10000, time(), attrs=SPECIFIC)


# Line 3
lastrow = [2, m, 0]
with prov.desc("L3 - list definition / assign", line=3):
    with prov.desc("L3 - list definition"):
        e_n2 = prov.entity("2", None, "literal", "2", attrs=HIDE)
        v_2 = prov.value("v2", "2", attrs=SPECIFIC)
        prov.defined(e_n2, v_2, time(), attrs=SPECIFIC)

        e_n0 = prov.entity("0", None, "literal", "0", attrs=HIDE)
        v_0 = prov.value("v0", "0", attrs=SPECIFIC)
        prov.defined(e_n0, v_0, time(), attrs=SPECIFIC)

        prov_lastrow = [e_n2, e_m, e_n0]
        prov_label = ["2", "m", "0"]

        e_list = prov.entity("list", None, "list", prov.calc_label(prov_label))

        ents = [
            (str(i), prov.VALUES[ent])
            for i, ent in enumerate(prov_lastrow)
        ]
        ti = time()
        v_list = prov.value("vlist", repr(lastrow), attrs=SPECIFIC)
        prov.derivedByInsertion(
            e_list, v_list, ents, ti, attrs=SPECIFIC
        )
        prov.defined(e_list, v_list, ti, attrs=SPECIFIC)

    with prov.desc("L3 - assign"):
        e_lastrow = prov.entity("lastrow", repr(lastrow), "Dictionary", "lastrow")
        prov.activity("assign", [(e_lastrow, e_list)], attrs=HIDE)
        prov.accessed(e_lastrow, v_list, time(), attrs=SPECIFIC)

# Line 4
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    lastrow
]
with prov.desc("L4 - list definition / assign", line=4):
    with prov.desc("L4 - list definition"):
        e_n1 = prov.entity("1", None, "literal", "1", attrs=HIDE)
        v_1 = prov.value("v1", "1", attrs=SPECIFIC)
        prov.defined(e_n1, v_1, time(), attrs=SPECIFIC)

        e_n4 = prov.entity("4", None, "literal", "4", attrs=HIDE)
        v_4 = prov.value("v4", "4", attrs=SPECIFIC)
        prov.defined(e_n4, v_4, time(), attrs=SPECIFIC)

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

        e_list = prov.entity("matrix", None, "list", prov.calc_label(prov_label))
        rows = []
        for i, row in enumerate(prov_dist):
            if isinstance(row, list):
                v_row = prov.value("row{}".format(i), repr(dist[i]), attrs=SPECIFIC)
                prov.derivedByInsertion(
                    e_list, v_row,
                    [(str(j), prov.VALUES[v]) for j, v in enumerate(row)],
                    time(), attrs=SPECIFIC
                )
                rows.append((str(i), v_row))
            else:
                rows.append((str(i), prov.VALUES[row]))
        ti = time()
        v_list = prov.value("vmatrix", repr(dist), attrs=SPECIFIC)
        prov.derivedByInsertion(
            e_list, v_list, rows, ti, attrs=SPECIFIC
        )
        prov.defined(e_list, v_list, ti, attrs=SPECIFIC)

    with prov.desc("L4 - assign"):
        e_dist = prov.entity("dist", None, "name", "dist")
        prov.accessed(e_dist, v_list, time(), attrs=SPECIFIC)
        prov.activity("assign", [(e_dist, e_list)], attrs=HIDE)

        e_result = prov.entity("result", None, "name", "result")
        prov.accessed(e_result, v_list, time(), attrs=SPECIFIC)
        prov.activity("assign", [(e_result, e_list)], attrs=HIDE)

# Line 9
# Algorithm

# Line 10
nodes = len(dist)
with prov.desc("L10 - func call / assign", line=10):
    e_ret = prov.entity("len_dist", None, "eval", "len(dist)")
    v_3 = prov.value("v3", "3", attrs=SPECIFIC)
    prov.defined(e_ret, v_3, time(), attrs=SPECIFIC)
    prov.activity("call", [], [e_dist], [e_ret], label="len", attrs=HIDE)

    e_nodes = prov.entity("nodes", None, "name", "nodes")
    prov.accessed(e_nodes, v_3, time(), attrs=SPECIFIC)
    prov.activity("assign", [(e_nodes, e_ret)], attrs=HIDE)

# Line 11
indexes = range(nodes)
with prov.desc("L11 - func call / list assign", line=11):
    e_ret = prov.entity("range_nodes", None, "eval", "range(nodes)")
    vs = [(str(i), prov.value("v{}".format(x), repr(x), attrs=SPECIFIC)) for i, x in enumerate(indexes)]
    v_range = prov.value("v_range", repr(list(indexes)), attrs=SPECIFIC)
    ti = time()
    prov.derivedByInsertion(
        e_ret, v_range, vs, ti, attrs=SPECIFIC
    )
    prov.defined(e_ret, v_range, ti, attrs=SPECIFIC)
    prov.activity("call", [], [e_nodes], [e_ret], label="range", attrs=HIDE)

    e_indexes = prov.entity("indexes", None, "name", "indexes")
    prov.accessed(e_indexes, v_range, time(), attrs=SPECIFIC)
    prov.activity("assign", [(e_indexes, e_ret)], attrs=HIDE)

# Line 12
for k in indexes:
    with prov.desc("L12 - loop access", line=12):
        e_k = prov.entity("k", None, "name", "k", show1=True, attrs=HIDE)
        v_k = prov.DICTS[v_range][repr(k)]
        prov.accessedPart(e_k, v_range, repr(k), v_k, time(), attrs=SPECIFIC)
        prov.activity("access", used=[e_indexes], generated=[e_k], attrs=HIDE)

    # Line 13
    distk = dist[k]
    with prov.desc("L13 - access / assign", line=13):
        e_dist_ak = prov.entity("dist@k", None, "access", "dist[k]", show1=True)
        v_dist_ak = prov.DICTS[v_list][repr(k)]
        prov.accessedPart(e_dist_ak, v_list, repr(k), v_dist_ak, time(), attrs=SPECIFIC)
        prov.activity("access", used=[e_dist, e_k], generated=[e_dist_ak], attrs=HIDE)

        e_distk = prov.entity("distk", None, "name", "distk", show1=True)
        prov.accessed(e_distk, v_dist_ak, time(), attrs=SPECIFIC)
        prov.activity("assign", [(e_distk, e_dist_ak)], attrs=HIDE)

    # Line 14
    for i in indexes:
        with prov.desc("L14 - loop access", line=14):
            e_i = prov.entity("i", None, "name", "i", show1=True, attrs=HIDE)
            v_i = prov.DICTS[v_range][repr(i)]
            prov.accessedPart(e_i, v_range, repr(i), v_i, time(), attrs=SPECIFIC)
            prov.activity("access", used=[e_indexes], generated=[e_i], attrs=HIDE)

        # Line 15
        with prov.desc("L15 - condition", line=15):
            cond([e_i, e_k])
        if i == k: continue

        # Line 16
        disti = dist[i]
        with prov.desc("L16 - access / assign", line=16):
            e_dist_ai = prov.entity("dist@i", None, "access", "dist[i]", show1=True)
            v_dist_ai = prov.DICTS[v_list][repr(i)]
            prov.accessedPart(e_dist_ai, v_list, repr(i), v_dist_ai, time(), attrs=SPECIFIC)
            prov.activity("access", used=[e_dist, e_i], generated=[e_dist_ai], attrs=HIDE)

            e_disti = prov.entity("disti", None, "name", "disti", show1=True)
            prov.accessed(e_disti, v_dist_ai, time(), attrs=SPECIFIC)
            prov.activity("assign", [(e_disti, e_dist_ai)], attrs=HIDE)

        # Line 17
        for j in indexes:
            with prov.desc("L17 - loop access", line=17):
                e_j = prov.entity("j", None, "name", "j", show1=True, attrs=HIDE)
                v_j = prov.DICTS[v_range][repr(j)]
                prov.accessedPart(e_j, v_range, repr(j), v_j, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_indexes], generated=[e_j], attrs=HIDE)

            # Line 18
            with prov.desc("L18 - condition", line=18):
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 19
            ikj = disti[k] + distk[j]
            with prov.desc("L19 - access / access / operation / assign", line=19):
                e_disti_ak = prov.entity("disti@k", None, "access", "disti[k]", show1=True, attrs=HIDE)
                v_disti_ak = prov.DICTS[v_dist_ai][repr(k)]
                prov.accessedPart(e_disti_ak, v_dist_ai, repr(k), v_disti_ak, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_disti, e_k], generated=[e_disti_ak], attrs=HIDE)

                e_distk_aj = prov.entity("distk@j", None, "access", "distk[j]", show1=True, attrs=HIDE)
                v_distk_aj = prov.DICTS[v_dist_ak][repr(j)]
                prov.accessedPart(e_distk_aj, v_dist_ak, repr(j), v_distk_aj, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_distk, e_j], generated=[e_distk_aj], attrs=HIDE)

                e_sum = prov.entity("sum", None, "operation", "disti[k] + distk[j]", show1=True, attrs=HIDE)
                vikj = prov.value("vsum", repr(ikj), attrs=SPECIFIC)
                prov.defined(e_sum, vikj, time(), attrs=SPECIFIC)
                prov.activity("+", [(e_sum, e_disti_ak, e_distk_aj)], attrs=HIDE)

                e_ikj = prov.entity("ikj", None, "name", "ikj", show1=True, attrs=HIDE)
                prov.accessed(e_ikj, vikj, time(), attrs=SPECIFIC)
                prov.activity("assign", [(e_ikj, e_sum)], attrs=HIDE)

            # Line 20
            with prov.desc("L20 - access", line=20):
                e_disti_aj = prov.entity("disti@j", None, "access", "disti[j]", show1=True, attrs=HIDE)
                v_disti_aj = prov.DICTS[v_dist_ai][repr(j)]
                prov.accessedPart(e_disti_aj, v_dist_ai, repr(j), v_disti_aj, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_disti, e_j], generated=[e_disti_aj], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 21
                disti[j] = ikj
                with prov.desc("L21 - part assign with propagation", line=21):
                    used = [e_j]
                    used += ucond # from if
                    generated = []

                    e_disti_aj = prov.entity("disti@j", None, "access", "disti[j]", show1=True)
                    ti = time()
                    prov.derivedByInsertion(
                        e_disti_aj, v_dist_ai,
                        [(str(j), vikj)],
                        ti, attrs=SPECIFIC
                    )
                    prov.accessed(e_disti_aj, vikj, ti, attrs=SPECIFIC)
                    prov.activity("assign", [(e_disti_aj, e_ikj)], used=[e_disti], shared=True)

# Line 22
print(result[0][2])
with prov.desc("L22 - access / access / call", line=22):
    e_result_a0 = prov.entity("result@0", None, "access", "result[0]", attrs=HIDE)
    v_result_a0 = prov.DICTS[v_list]["0"]
    prov.accessedPart(e_result_a0, v_list, "0", v_result_a0, time(), attrs=SPECIFIC)
    prov.activity("access", used=[e_result, e_n0], generated=[e_result_a0], attrs=HIDE)


    e_result_a02 = prov.entity("result@0@2", None, "access", "result[0][2]", attrs=HIDE)
    v_result_a02 = prov.DICTS[v_result_a0]["2"]
    prov.accessedPart(e_result_a02, v_result_a0, "2", v_result_a02, time(), attrs=SPECIFIC)
    prov.activity("access", used=[e_result_a0, e_n2], generated=[e_result_a02], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

prov.finish(show_count=False)
