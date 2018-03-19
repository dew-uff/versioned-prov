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

x = 0
LAST = None

def time():
    global x, LAST
    x += 1
    return x
    current = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    while current == LAST:
        current = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    LAST = current
    return current

def cond(ents):
    return ents

def get_item(ent, pos):
    follow_ref = prov.SAME[ent]
    return prov.DICTS[follow_ref][str(pos)]

def use(ents, extra={}, checkpoint=None):
    checkpoint = checkpoint or time()
    return prov.Use(*ents, attrs=dict(
        **{prov.NAMESPACE + "checkpoint": checkpoint},
        **extra
    ))

def generate(ents, extra={}, checkpoint=None):
    checkpoint = checkpoint or time()
    return prov.Generation(*ents, attrs=dict(
        **{prov.NAMESPACE + "checkpoint": checkpoint},
        **extra
    ))

# Line 1
# Input graph

# Line 2
m = 10000 # max value
with prov.desc("L2 - assign", line=2):
    e_n10000 = prov.entity("10000", "10000", "literal", None, attrs=HIDE)

    e_m = prov.entity("m", "10000", "name", "m")
    prov.activity("assign", [prov.RefDerivation(time(), e_m, e_n10000, attrs=HIDE)], attrs=HIDE)

# Line 3
lastrow = [2, m, 0]
with prov.desc("L3 - list definition / assign", line=3):
    with prov.desc("L3 - list definition"):
        e_n2 = prov.entity("2", "2", "literal", None)
        e_n0 = prov.entity("0", "0", "literal", None)

        prov_lastrow = [e_n2, e_m, e_n0]
        prov_label = ["2", "m", "0"]

        ti = time()
        e_list = prov.entity("list", repr(lastrow), "list", prov.calc_label(prov_label))
        for i, pent in enumerate(prov_lastrow):
            prov.vhadMember(e_list, pent, str(i), ti, attrs=SPECIFIC)

    with prov.desc("L3 - assign"):
        e_lastrow = prov.entity("lastrow", repr(lastrow), "name", "lastrow")
        prov.activity("assign", [prov.RefDerivation(time(), e_lastrow, e_list, attrs=HIDE)], attrs=HIDE)

# Line 4
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    lastrow,
]
with prov.desc("L4 - list definition / assign", line=4):
    with prov.desc("L4 - list definition"):
        e_n1 = prov.entity("1", "1", "literal", None)
        e_n4 = prov.entity("4", "4", "literal", None)

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

        e_list = prov.entity("matrix", repr(dist), "list", prov.calc_label(prov_label))
        for i, (pdist, plabel) in enumerate(zip(prov_dist, prov_label)):
            if isinstance(pdist, list):
                e_row = prov.entity("matrix{}".format(i), repr(dist[i]), "list", prov.calc_label(plabel))
                for j, ppdist in enumerate(pdist):
                    prov.vhadMember(e_row, ppdist, str(j), ti, attrs=SPECIFIC)
            else:
                e_row = pdist
            prov.vhadMember(e_list, e_row, str(i), ti, attrs=SPECIFIC)

    with prov.desc("L4 - assign"):
        e_dist = prov.entity("dist", repr(dist), "name", "dist")
        prov.activity("assign", [prov.RefDerivation(time(), e_dist, e_list, attrs=HIDE)], attrs=HIDE)

        e_result = prov.entity("result", repr(result), "name", "result")
        prov.activity("assign", [prov.RefDerivation(time(), e_result, e_list, attrs=HIDE)], attrs=HIDE)


# Line 9
# Algorithm



# Line 10
nodes = len(dist)
with prov.desc("L10 - func call / assign", line=10):
    e_ret = prov.entity("len_dist", repr(nodes), "eval", "len(dist)", attrs=HIDE)
    prov.activity("call", [], [use([e_dist], HIDE)], [generate([e_ret], HIDE)], label="len", attrs=HIDE)

    e_nodes = prov.entity("nodes", repr(nodes), "name", "nodes", attrs=HIDE)
    prov.activity("assign", [prov.RefDerivation(time(), e_nodes, e_ret, attrs=HIDE)], attrs=HIDE)


# Line 11
indexes = range(nodes)
with prov.desc("L11 - func call / list assign", line=11):
    ti = time()
    e_ret = prov.entity("range_nodes", repr(list(indexes)), "eval", "range(nodes)")
    e_items = []
    for i in indexes:
        e_item = prov.entity("range_nodes{}".format(i), str(i), "item", None)
        prov.vhadMember(e_ret, e_item, str(i), ti, attrs=SPECIFIC)
        e_items.append(e_item)
    prov.activity("call", [], [e_nodes], [generate([e_ret] + e_items, HIDE, checkpoint=ti)], label="range", attrs=HIDE)

    e_indexes = prov.entity("indexes", repr(list(indexes)), "name", "indexes")
    prov.activity("assign", [prov.RefDerivation(time(), e_indexes, e_ret, attrs=HIDE)], attrs=HIDE)

# Line 12
for k in indexes:
    with prov.desc("L12 - loop access", line=12):
        e_k = prov.entity("k", k, "name", "k", show1=True, attrs=HIDE)
        item = get_item(e_indexes, k)
        prov.activity("access", [prov.AccessDerivation(time(), e_indexes, str(k), e_k, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

    # Line 13
    distk = dist[k]
    with prov.desc("L13 - access / assign", line=13):
        e_dist_ak = prov.entity("dist@k", repr(distk), "access", "dist[k]", show1=True)
        item = get_item(e_dist, k)
        prov.activity("access", [prov.AccessDerivation(time(), e_dist, str(k), e_dist_ak, item, attrs=HIDE)], used=[e_dist, e_k], attrs=HIDE)

        e_distk = prov.entity("distk", repr(distk), "name", "distk", show1=True)
        prov.activity("assign", [prov.RefDerivation(time(), e_distk, e_dist_ak, attrs=HIDE)], attrs=HIDE)

    # Line 14
    for i in indexes:
        with prov.desc("L14 - loop access", line=14):
            e_i = prov.entity("i", i, "name", "i", show1=True, attrs=HIDE)
            item = get_item(e_indexes, i)
            prov.activity("access", [prov.AccessDerivation(time(), e_indexes, str(i), e_i, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

        # Line 15
        with prov.desc("L15 - condition", line=15):
            cond([e_i, e_k])
        if i == k: continue

        # Line 16
        disti = dist[i]
        with prov.desc("L16 - access / assign", line=16):
            e_dist_ai = prov.entity("dist@i", repr(disti), "access", "dist[i]", show1=True)
            item = get_item(e_dist, i)
            prov.activity("access", [prov.AccessDerivation(time(), e_dist, str(i), e_dist_ai, item, attrs=HIDE)], used=[e_dist, e_i], attrs=HIDE)

            e_disti = prov.entity("disti", repr(disti), "name", "disti", show1=True)
            prov.activity("assign", [prov.RefDerivation(time(), e_disti, e_dist_ai, attrs=HIDE)], attrs=HIDE)

        # Line 17
        for j in indexes:
            with prov.desc("L17 - loop access", line=17):
                e_j = prov.entity("j", j, "name", "j", show1=True, attrs=HIDE)
                item = get_item(e_indexes, j)
                prov.activity("access", [prov.AccessDerivation(time(), e_indexes, str(j), e_j, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

            # Line 18
            with prov.desc("L18 - condition", line=18):
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 19
            ikj = disti[k] + distk[j]
            with prov.desc("L19 - access / access / operation / assign", line=19):
                e_disti_ak = prov.entity("disti@k", repr(disti[k]), "access", "disti[k]", show1=True, attrs=HIDE)
                item = get_item(e_disti, k)
                prov.activity("access", [prov.AccessDerivation(time(), e_disti, str(k), e_disti_ak, item, attrs=HIDE)], used=[e_disti, e_k], attrs=HIDE)

                e_distk_aj = prov.entity("distk@j", repr(distk[j]), "access", "distk[j]", show1=True, attrs=HIDE)
                item = get_item(e_distk, j)
                prov.activity("access", [prov.AccessDerivation(time(), e_distk, str(j), e_distk_aj, item, attrs=HIDE)], used=[e_distk, e_j], attrs=HIDE)

                e_sum = prov.entity("sum", repr(ikj), "operation", "disti[k] + distk[j]", show1=True, attrs=HIDE)
                prov.activity("+", [prov.TimeDerivation(time(), e_sum, e_disti_ak, e_distk_aj, attrs=HIDE)], attrs=HIDE)

                e_ikj = prov.entity("ikj", repr(ikj), "name", "ikj", show1=True, attrs=HIDE)
                prov.activity("assign", [prov.RefDerivation(time(), e_ikj, e_sum, attrs=HIDE)], attrs=HIDE)

            # Line 20
            with prov.desc("L20 - access", line=20):
                e_disti_aj = prov.entity("disti@j", repr(disti[j]), "access", "disti[j]", show1=True, attrs=HIDE)
                item = get_item(e_disti, j)
                prov.activity("access", [prov.AccessDerivation(time(), e_disti, str(k), e_disti_aj, item, attrs=HIDE)], used=[e_disti, e_j], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 21
                disti[j] = ikj
                with prov.desc("L21 - part assign with propagation", line=21):
                    derived = []
                    used = [use([e_disti], SPECIFIC), e_j]
                    used += ucond # from if
                    generated = []

                    ti = time()
                    e_disti_aj = prov.entity("disti@j", repr(ikj), "access", "disti[j]", show1=True)
                    follow_ref = prov.SAME[e_disti]
                    prov.vhadMember(follow_ref, e_disti_aj, str(j), ti, attrs=SPECIFIC)

                    prov.activity("assign", [prov.WriteDerivation(ti, e_disti, str(j), e_disti_aj, e_ikj)], used=used)


# Line 22
print(result[0][2])
with prov.desc("L22 - access / access / call", line=22):
    e_result_a0 = prov.entity("result@0", repr(result[0]), "access", "result[0]", attrs=HIDE)
    item = get_item(e_result, "0")
    prov.activity("access", [prov.AccessDerivation(time(), e_result, "0", e_result_a0, item, attrs=HIDE)], used=[e_result, e_n0], attrs=HIDE)

    e_result_a02 = prov.entity("result@0@2", repr(result[0][2]), "access", "result[0][2]", attrs=HIDE)
    item = get_item(e_result_a0, "2")
    prov.activity("access", [prov.AccessDerivation(time(), e_result_a0, "2", e_result_a02, item, attrs=HIDE)], used=[e_result_a0, e_n2], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

prov.finish(show_count=False)
