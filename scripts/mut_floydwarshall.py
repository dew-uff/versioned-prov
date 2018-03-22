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
m = 10000 # max value
with prov.desc("L1 - assign", line=1) as line:
    e_n10000 = prov.entity("10000", None, prov.SCRIPT + "literal", "10000", line, attrs=HIDE)
    v_10000 = prov.value("v10000", "10000", attrs=SPECIFIC)
    prov.defined(e_n10000, v_10000, time(), attrs=SPECIFIC)

    e_m = prov.entity("m", None, prov.SCRIPT + "name", "m", line, attrs=HIDE)
    prov.activity("assign", [(e_m, e_n10000)], attrs=HIDE)
    prov.accessed(e_m, v_10000, time(), attrs=SPECIFIC)

# Line 2
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    [2, m, 0]
]
with prov.desc("L2 - list definition / assign", line=2) as line:
    with prov.desc("L2 - list definition"):
        e_n0 = prov.entity("0", None, prov.SCRIPT + "literal", "0", line + 1, attrs=HIDE)
        v_0 = prov.value("v0", "0", attrs=SPECIFIC)
        prov.defined(e_n0, v_0, time(), attrs=SPECIFIC)

        e_n1 = prov.entity("1", None, prov.SCRIPT + "literal", "1", line + 1, attrs=HIDE)
        v_1 = prov.value("v1", "1", attrs=SPECIFIC)
        prov.defined(e_n1, v_1, time(), attrs=SPECIFIC)

        e_n4 = prov.entity("4", None, prov.SCRIPT + "literal", "4", line + 1, attrs=HIDE)
        v_4 = prov.value("v4", "4", attrs=SPECIFIC)
        prov.defined(e_n4, v_4, time(), attrs=SPECIFIC)

        e_n2 = prov.entity("2", None, prov.SCRIPT + "literal", "2", line + 2, attrs=HIDE)
        v_2 = prov.value("v2", "2", attrs=SPECIFIC)
        prov.defined(e_n2, v_2, time(), attrs=SPECIFIC)

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

        e_list = prov.entity("matrix", None, prov.SCRIPT + "list", prov.calc_label(prov_label), line)
        rows = []
        for i, row in enumerate(prov_dist):
            v_row = prov.value("row{}".format(i), repr(dist[i]), attrs=SPECIFIC)
            prov.derivedByInsertion(
                e_list, v_row,
                [(str(j), prov.VALUES[v]) for j, v in enumerate(row)],
                time(), attrs=SPECIFIC
            )
            rows.append((str(i), v_row))
        ti = time()
        v_list = prov.value("vmatrix", repr(dist), attrs=SPECIFIC)
        prov.derivedByInsertion(
            e_list, v_list, rows, ti, attrs=SPECIFIC
        )
        prov.defined(e_list, v_list, ti, attrs=SPECIFIC)

    with prov.desc("L2 - assign"):
        e_dist = prov.entity("dist", None, prov.SCRIPT + "name", "dist", line)
        prov.accessed(e_dist, v_list, time(), attrs=SPECIFIC)
        prov.activity("assign", [(e_dist, e_list)], attrs=HIDE)

        e_result = prov.entity("result", None, prov.SCRIPT + "name", "result", line)
        prov.accessed(e_result, v_list, time(), attrs=SPECIFIC)
        prov.activity("assign", [(e_result, e_list)], attrs=HIDE)

# Line 6
nodes = len(dist)
with prov.desc("L6 - func call / assign", line=6) as line:
    e_ret = prov.entity("len_dist", None, prov.SCRIPT + "eval", "len(dist)", line)
    v_3 = prov.value("v3", "3", attrs=SPECIFIC)
    prov.defined(e_ret, v_3, time(), attrs=SPECIFIC)
    prov.activity("call", [], [e_dist], [e_ret], label="len", attrs=HIDE)

    e_nodes = prov.entity("nodes", None, prov.SCRIPT + "name", "nodes", line)
    prov.accessed(e_nodes, v_3, time(), attrs=SPECIFIC)
    prov.activity("assign", [(e_nodes, e_ret)], attrs=HIDE)

# Line 7
indexes = range(nodes)
with prov.desc("L7 - func call / list assign", line=7) as line:
    e_ret = prov.entity("range_nodes", None, prov.SCRIPT + "eval", "range(nodes)", line)
    vs = [(str(i), prov.value("v{}".format(x), repr(x), attrs=SPECIFIC)) for i, x in enumerate(indexes)]
    v_range = prov.value("v_range", repr(list(indexes)), attrs=SPECIFIC)
    ti = time()
    prov.derivedByInsertion(
        e_ret, v_range, vs, ti, attrs=SPECIFIC
    )
    prov.defined(e_ret, v_range, ti, attrs=SPECIFIC)
    prov.activity("call", [], [e_nodes], [e_ret], label="range", attrs=HIDE)

    e_indexes = prov.entity("indexes", None, prov.SCRIPT + "name", "indexes", line)
    prov.accessed(e_indexes, v_range, time(), attrs=SPECIFIC)
    prov.activity("assign", [(e_indexes, e_ret)], attrs=HIDE)

# Line 8
for k in indexes:
    with prov.desc("L8 - loop access", line=8) as line:
        e_k = prov.entity("k", None, prov.SCRIPT + "name", "k", line, show1=True, attrs=HIDE)
        v_k = prov.DICTS[v_range][repr(k)]
        prov.accessedPart(e_k, v_range, repr(k), v_k, time(), attrs=SPECIFIC)
        prov.activity("access", used=[e_indexes], generated=[e_k], attrs=HIDE)

    # Line 9
    distk = dist[k]
    with prov.desc("L9 - access / assign", line=9) as line:
        e_dist_ak = prov.entity("dist@k", None, prov.SCRIPT + "access", "dist[k]", line, show1=True)
        v_dist_ak = prov.DICTS[v_list][repr(k)]
        prov.accessedPart(e_dist_ak, v_list, repr(k), v_dist_ak, time(), attrs=SPECIFIC)
        prov.activity("access", used=[e_dist, e_k], generated=[e_dist_ak], attrs=HIDE)

        e_distk = prov.entity("distk", None, prov.SCRIPT + "name", "distk", line, show1=True)
        prov.accessed(e_distk, v_dist_ak, time(), attrs=SPECIFIC)
        prov.activity("assign", [(e_distk, e_dist_ak)], attrs=HIDE)

    # Line 10
    for i in indexes:
        with prov.desc("L10 - loop access", line=10) as line:
            e_i = prov.entity("i", None, prov.SCRIPT + "name", "i", line, show1=True, attrs=HIDE)
            v_i = prov.DICTS[v_range][repr(i)]
            prov.accessedPart(e_i, v_range, repr(i), v_i, time(), attrs=SPECIFIC)
            prov.activity("access", used=[e_indexes], generated=[e_i], attrs=HIDE)

        # Line 11
        with prov.desc("L11 - condition", line=11) as line:
            cond([e_i, e_k])
        if i == k: continue

        # Line 12
        disti = dist[i]
        with prov.desc("L12 - access / assign", line=12) as line:
            e_dist_ai = prov.entity("dist@i", None, prov.SCRIPT + "access", "dist[i]", line, show1=True)
            v_dist_ai = prov.DICTS[v_list][repr(i)]
            prov.accessedPart(e_dist_ai, v_list, repr(i), v_dist_ai, time(), attrs=SPECIFIC)
            prov.activity("access", used=[e_dist, e_i], generated=[e_dist_ai], attrs=HIDE)

            e_disti = prov.entity("disti", None, prov.SCRIPT + "name", "disti", line, show1=True)
            prov.accessed(e_disti, v_dist_ai, time(), attrs=SPECIFIC)
            prov.activity("assign", [(e_disti, e_dist_ai)], attrs=HIDE)

        # Line 13
        for j in indexes:
            with prov.desc("L13 - loop access", line=13) as line:
                e_j = prov.entity("j", None, prov.SCRIPT + "name", "j", line, show1=True, attrs=HIDE)
                v_j = prov.DICTS[v_range][repr(j)]
                prov.accessedPart(e_j, v_range, repr(j), v_j, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_indexes], generated=[e_j], attrs=HIDE)

            # Line 14
            with prov.desc("L14 - condition", line=14) as line:
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 15
            ikj = disti[k] + distk[j]
            with prov.desc("L15 - access / access / operation / assign", line=15) as line:
                e_disti_ak = prov.entity("disti@k", None, prov.SCRIPT + "access", "disti[k]", line, show1=True, attrs=HIDE)
                v_disti_ak = prov.DICTS[v_dist_ai][repr(k)]
                prov.accessedPart(e_disti_ak, v_dist_ai, repr(k), v_disti_ak, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_disti, e_k], generated=[e_disti_ak], attrs=HIDE)

                e_distk_aj = prov.entity("distk@j", None, prov.SCRIPT + "access", "distk[j]", line, show1=True, attrs=HIDE)
                v_distk_aj = prov.DICTS[v_dist_ak][repr(j)]
                prov.accessedPart(e_distk_aj, v_dist_ak, repr(j), v_distk_aj, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_distk, e_j], generated=[e_distk_aj], attrs=HIDE)

                e_sum = prov.entity("sum", None, prov.SCRIPT + "operation", "disti[k] + distk[j]", line, show1=True, attrs=HIDE)
                vikj = prov.value("vsum", repr(ikj), attrs=SPECIFIC)
                prov.defined(e_sum, vikj, time(), attrs=SPECIFIC)
                prov.activity("+", [(e_sum, e_disti_ak, e_distk_aj)], attrs=HIDE)

                e_ikj = prov.entity("ikj", None, prov.SCRIPT + "name", "ikj", line, show1=True, attrs=HIDE)
                prov.accessed(e_ikj, vikj, time(), attrs=SPECIFIC)
                prov.activity("assign", [(e_ikj, e_sum)], attrs=HIDE)

            # Line 16
            with prov.desc("L16 - access", line=16) as line:
                e_disti_aj = prov.entity("disti@j", None, prov.SCRIPT + "access", "disti[j]", line, show1=True, attrs=HIDE)
                v_disti_aj = prov.DICTS[v_dist_ai][repr(j)]
                prov.accessedPart(e_disti_aj, v_dist_ai, repr(j), v_disti_aj, time(), attrs=SPECIFIC)
                prov.activity("access", used=[e_disti, e_j], generated=[e_disti_aj], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 17
                disti[j] = ikj
                with prov.desc("L17 - part assign with propagation", line=17) as line:
                    used = [e_j]
                    used += ucond # from if
                    generated = []

                    e_disti_aj = prov.entity("disti@j", None, prov.SCRIPT + "access", "disti[j]", line, show1=True)
                    ti = time()
                    prov.derivedByInsertion(
                        e_disti_aj, v_dist_ai,
                        [(str(j), vikj)],
                        ti, attrs=SPECIFIC
                    )
                    prov.accessed(e_disti_aj, vikj, ti, attrs=SPECIFIC)
                    prov.activity("assign", [(e_disti_aj, e_ikj)], used=[e_disti], shared=True)

# Line 18
print(result[0][2])
with prov.desc("L18 - access / access / call", line=18) as line:
    e_result_a0 = prov.entity("result@0", None, prov.SCRIPT + "access", "result[0]", line, attrs=HIDE)
    v_result_a0 = prov.DICTS[v_list]["0"]
    prov.accessedPart(e_result_a0, v_list, "0", v_result_a0, time(), attrs=SPECIFIC)
    prov.activity("access", used=[e_result, e_n0], generated=[e_result_a0], attrs=HIDE)


    e_result_a02 = prov.entity("result@0@2", None, prov.SCRIPT + "access", "result[0][2]", line, attrs=HIDE)
    v_result_a02 = prov.DICTS[v_result_a0]["2"]
    prov.accessedPart(e_result_a02, v_result_a0, "2", v_result_a02, time(), attrs=SPECIFIC)
    prov.activity("access", used=[e_result_a0, e_n2], generated=[e_result_a02], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

prov.finish(show_count=False)
