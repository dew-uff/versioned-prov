from datetime import datetime
from pprint import pprint
import sys
sys.path.insert(0, '..')

import tools.view.versioned_prov
import tools.annotations as prov

prov.reset_prov("../generated/versioned_prov/")
prov.STATS_VIEW = 1
prov.NAMESPACE = "version:"

HIDE = prov.HIDE
SPECIFIC = prov.SPECIFIC

def time():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

def cond(ents):
    return ents

def get_item(ent, pos):
    follow_ref = prov.SAME[ent]
    return prov.DICTS[follow_ref][str(pos)]

# Line 1
# Input graph

# Line 2
m = 10000 # max value
with prov.desc("L2 - assign", line=2):
    e_n10000 = prov.ventity(time(), "10000", "10000", "literal", None, attrs=HIDE)

    ti = time()
    e_m = prov.ventity(ti, "m", "10000", "name", "m")
    prov.activity("assign", [prov.RefDerivation(ti, e_m, e_n10000, attrs=HIDE)], attrs=HIDE)

# Line 3
lastrow = [2, m, 0]
with prov.desc("L3 - list definition / assign", line=3):
    with prov.desc("L3 - list definition"):
        e_n2 = prov.ventity(time(), "2", "2", "literal", None)
        e_n0 = prov.ventity(time(), "0", "0", "literal", None)

        prov_lastrow = [e_n2, e_m, e_n0]
        prov_label = ["2", "m", "0"]

        ti = time()
        e_list = prov.ventity(ti, "list", repr(lastrow), "list", prov.calc_label(prov_label))
        for i, pent in enumerate(prov_lastrow):
            prov.vhadMember(e_list, pent, str(i), ti, attrs=SPECIFIC)

    with prov.desc("L3 - assign"):
        ti = time()
        e_lastrow = prov.ventity(ti, "lastrow", repr(lastrow), "name", "lastrow")
        prov.activity("assign", [prov.RefDerivation(ti, e_lastrow, e_list, attrs=HIDE)], attrs=HIDE)

# Line 4
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    lastrow,
]
with prov.desc("L4 - list definition / assign", line=4):
    with prov.desc("L4 - list definition"):
        e_n1 = prov.ventity(time(), "1", "1", "literal", None)
        e_n4 = prov.ventity(time(), "4", "4", "literal", None)

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

        ti = time()

        e_list = prov.ventity(ti, "matrix", repr(dist), "list", prov.calc_label(prov_label))
        for i, (pdist, plabel) in enumerate(zip(prov_dist, prov_label)):
            if isinstance(pdist, list):
                e_row = prov.ventity(ti, "list{}".format(i), repr(dist[i]), "list", prov.calc_label(plabel))
                for j, ppdist in enumerate(pdist):
                    prov.vhadMember(e_row, ppdist, str(j), ti, attrs=SPECIFIC)
            else:
                e_row = pdist
            prov.vhadMember(e_list, e_row, str(i), ti, attrs=SPECIFIC)

    with prov.desc("L4 - assign"):
        ti = time()
        e_dist = prov.ventity(ti, "dist", repr(dist), "name", "dist")
        prov.activity("assign", [prov.RefDerivation(ti, e_dist, e_list, attrs=HIDE)], attrs=HIDE)

        ti = time()
        e_result = prov.ventity(ti, "result", repr(result), "name", "result")
        prov.activity("assign", [prov.RefDerivation(ti, e_result, e_list, attrs=HIDE)], attrs=HIDE)


# Line 9
# Algorithm

# Line 10
nodes = len(dist)
with prov.desc("L10 - func call / assign", line=10):
    e_ret = prov.ventity(time(), "len_dist", repr(nodes), "eval", "len(dist)", attrs=HIDE)
    prov.activity("call", [], [e_dist], [e_ret], label="len", attrs=HIDE)

    ti = time()
    e_nodes = prov.ventity(ti, "nodes", repr(nodes), "name", "nodes", attrs=HIDE)
    prov.activity("assign", [prov.RefDerivation(ti, e_nodes, e_ret, attrs=HIDE)], attrs=HIDE)


# Line 11
indexes = range(nodes)
with prov.desc("L11 - func call / list assign", line=11):
    ti = time()
    e_ret = prov.ventity(ti, "range_nodes", repr(list(indexes)), "eval", "range(nodes)")
    e_items = []
    for i in indexes:
        e_item = prov.ventity(ti, "range_nodes{}".format(i), str(i), "item", None)
        prov.vhadMember(e_ret, e_item, str(i), ti, attrs=SPECIFIC)
        e_items.append(e_item)
    prov.activity("call", [], [e_nodes], [e_ret] + e_items, label="range", attrs=HIDE)

    ti = time()
    e_indexes = prov.ventity(ti, "indexes", repr(list(indexes)), "name", "indexes")
    prov.activity("assign", [prov.RefDerivation(ti, e_indexes, e_ret, attrs=HIDE)], attrs=HIDE)

# Line 12
for k in indexes:
    with prov.desc("L12 - loop access", line=12):
        ti = time()
        e_k = prov.ventity(ti, "k", k, "name", "k", attrs=HIDE)
        item = get_item(e_indexes, k)
        prov.activity("access", [prov.AccessDerivation(ti, e_indexes, str(k), e_k, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

    # Line 13
    distk = dist[k]
    with prov.desc("L13 - access / assign", line=13):
        ti = time()
        e_dist_ak = prov.ventity(ti, "dist_ak", repr(distk), "access", "dist[k]")
        item = get_item(e_dist, k)
        prov.activity("access", [prov.AccessDerivation(ti, e_dist, str(k), e_dist_ak, item, attrs=HIDE)], used=[e_dist, e_k], attrs=HIDE)

        ti = time()
        e_distk = prov.ventity(ti, "distk", repr(distk), "name", "distk")
        prov.activity("assign", [prov.RefDerivation(ti, e_distk, e_dist_ak, attrs=HIDE)], attrs=HIDE)

    # Line 14
    for i in indexes:
        with prov.desc("L14 - loop access", line=14):
            ti = time()
            e_i = prov.ventity(ti, "i", i, "name", "i", attrs=HIDE)
            item = get_item(e_indexes, i)
            prov.activity("access", [prov.AccessDerivation(ti, e_indexes, str(i), e_i, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

        # Line 15
        with prov.desc("L15 - condition", line=15):
            cond([e_i, e_k])
        if i == k: continue

        # Line 16
        disti = dist[i]
        with prov.desc("L16 - access / assign", line=16):
            ti = time()
            e_dist_ai = prov.ventity(ti, "dist_ai", repr(disti), "access", "dist[i]")
            item = get_item(e_dist, i)
            prov.activity("access", [prov.AccessDerivation(ti, e_dist, str(i), e_dist_ai, item, attrs=HIDE)], used=[e_dist, e_i], attrs=HIDE)

            ti = time()
            e_disti = prov.ventity(ti, "disti", repr(disti), "name", "disti")
            prov.activity("assign", [prov.RefDerivation(ti, e_disti, e_dist_ai, attrs=HIDE)], attrs=HIDE)

        # Line 17
        for j in indexes:
            with prov.desc("L17 - loop access", line=17):
                ti = time()
                e_j = prov.ventity(ti, "j", j, "name", "j", attrs=HIDE)
                item = get_item(e_indexes, j)
                prov.activity("access", [prov.AccessDerivation(ti, e_indexes, str(j), e_j, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

            # Line 18
            with prov.desc("L18 - condition", line=18):
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 19
            ikj = disti[k] + distk[j]
            with prov.desc("L19 - access / access / operation / assign", line=19):
                ti = time()
                e_disti_ak = prov.ventity(ti, "disti_ak", repr(disti[k]), "access", "disti[k]", attrs=HIDE)
                item = get_item(e_disti, k)
                prov.activity("access", [prov.AccessDerivation(ti, e_disti, str(k), e_disti_ak, item, attrs=HIDE)], used=[e_disti, e_k], attrs=HIDE)

                ti = time()
                e_distk_aj = prov.ventity(ti, "distk_aj", repr(distk[j]), "access", "distk[j]", attrs=HIDE)
                item = get_item(e_distk, j)
                prov.activity("access", [prov.AccessDerivation(ti, e_distk, str(j), e_distk_aj, item, attrs=HIDE)], used=[e_distk, e_j], attrs=HIDE)

                e_sum = prov.ventity(time(), "sum", repr(ikj), "operation", "disti[k] + distk[j]", attrs=HIDE)
                prov.activity("+", [(e_sum, e_disti_ak, e_distk_aj)], attrs=HIDE)

                ti = time()
                e_ikj = prov.ventity(ti, "ikj", repr(ikj), "name", "ikj", attrs=HIDE)
                prov.activity("assign", [prov.RefDerivation(ti, e_ikj, e_sum, attrs=HIDE)], attrs=HIDE)

            # Line 20
            with prov.desc("L20 - access", line=20):
                ti = time()
                e_disti_aj = prov.ventity(ti, "disti_aj", repr(disti[j]), "access", "disti[j]", attrs=HIDE)
                item = get_item(e_disti, j)
                prov.activity("access", [prov.AccessDerivation(ti, e_disti, str(k), e_disti_aj, item, attrs=HIDE)], used=[e_disti, e_j], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 21
                disti[j] = ikj
                with prov.desc("L21 - part assign with propagation", line=21):
                    derived = []
                    used = [prov.Use(e_disti, attrs=SPECIFIC), e_j]
                    used += ucond # from if
                    generated = []

                    ti = time()
                    e_disti_aj = prov.ventity(ti, "disti_aj", repr(ikj), "access", "disti[j]")
                    follow_ref = prov.SAME[e_disti]
                    prov.vhadMember(follow_ref, e_disti_aj, str(j), ti, attrs=SPECIFIC)

                    prov.activity("assign", [prov.WriteDerivation(ti, e_disti, str(j), e_disti_aj, e_ikj)], used=used)


# Line 22
print(result[0][2])
with prov.desc("L22 - access / access / call", line=22):
    ti = time()
    e_result_a0 = prov.ventity(ti, "result_a0", repr(result[0]), "access", "result[0]", attrs=HIDE)
    item = get_item(e_result, "0")
    prov.activity("access", [prov.AccessDerivation(ti, e_result, "0", e_result_a0, item, attrs=HIDE)], used=[e_result, e_n0], attrs=HIDE)

    ti = time()
    e_result_a02 = prov.ventity(ti, "result_a02", repr(result[0][2]), "access", "result[0][2]", attrs=HIDE)
    item = get_item(e_result_a0, "2")
    prov.activity("access", [prov.AccessDerivation(ti, e_result_a0, "2", e_result_a02, item, attrs=HIDE)], used=[e_result_a0, e_n2], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

prov.finish(show_count=False)
