from datetime import datetime
from pprint import pprint

import extensible_provn.view.intertwined_prov
import annotations as prov

prov.reset_prov("../generated/intertwined_prov/")
prov.STATS_VIEW = 1
prov.NAMESPACE = "intertwined:"

HIDE = prov.HIDE
SPECIFIC = prov.SPECIFIC

def time():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

def cond(ents):
    return ents

def get_item(ent, pos):
    follow_ref = prov.SAME[ent]
    follow_value = prov.VALUES[follow_ref]
    return prov.DICTS[follow_value][str(pos)]

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
m = 10000 # max value

with prov.desc("L1 - assign", line=1) as line:
    e_n10000 = prov.entity("10000", "10000", prov.SCRIPT + "literal", None, line, attrs=HIDE)
    prov.specializationOf(e_n10000, prov.version(e_n10000, time(), attrs=SPECIFIC), attrs=SPECIFIC)

    e_m = prov.entity("m", "10000", prov.SCRIPT + "name", "m", line)
    prov.activity("assign", [prov.RefDerivation(time(), e_m, e_n10000, attrs=HIDE)], attrs=HIDE)

# Line 2
result = dist = [
    [0, 1, 4],
    [m, 0, 2],
    [2, m, 0]]
with prov.desc("L2 - list definition / assign", line=2) as line:
    with prov.desc("L2 - list definition"):
        e_n0 = prov.entity("0", "0", prov.SCRIPT + "literal", None, line + 1)
        prov.specializationOf(e_n0, prov.version(e_n0, time(), attrs=SPECIFIC), attrs=SPECIFIC)
        e_n1 = prov.entity("1", "1", prov.SCRIPT + "literal", None, line + 1)
        prov.specializationOf(e_n1, prov.version(e_n1, time(), attrs=SPECIFIC), attrs=SPECIFIC)
        e_n4 = prov.entity("4", "4", prov.SCRIPT + "literal", None, line + 1)
        prov.specializationOf(e_n4, prov.version(e_n4, time(), attrs=SPECIFIC), attrs=SPECIFIC)
        e_n2 = prov.entity("2", "2", prov.SCRIPT + "literal", None, line + 2)
        prov.specializationOf(e_n2, prov.version(e_n2, time(), attrs=SPECIFIC), attrs=SPECIFIC)


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

        ti = time()

        e_list = prov.entity("list", repr(dist), prov.SCRIPT + "list", prov.calc_label(prov_label), line)
        e_list_v = prov.version(e_list, ti, attrs=SPECIFIC)
        prov.specializationOf(e_list, e_list_v, attrs=SPECIFIC)

        for i, (pdist, plabel) in enumerate(zip(prov_dist, prov_label)):
            e_row = prov.entity("list{}".format(i), repr(dist[i]), prov.SCRIPT + "list", prov.calc_label(plabel), line + i + 1)
            e_row_v = prov.version(e_row, ti, attrs=SPECIFIC)
            prov.specializationOf(e_row, e_row_v, attrs=SPECIFIC)
            prov.hadDictionaryMember(e_list_v, e_row, str(i), attrs=SPECIFIC)
            for j, (ppdist, pplabel) in enumerate(zip(pdist, plabel)):
                prov.hadDictionaryMember(e_row_v, ppdist, str(j), attrs=SPECIFIC)

    with prov.desc("L2 - assign"):
        e_dist = prov.entity("dist", repr(dist), prov.SCRIPT + "name", "dist", line)
        prov.activity("assign", [prov.RefDerivation(time(), e_dist, e_list, attrs=HIDE)], attrs=HIDE)

        e_result = prov.entity("result", repr(result), prov.SCRIPT + "name", "result", line)
        prov.activity("assign", [prov.RefDerivation(time(), e_result, e_list, attrs=HIDE)], attrs=HIDE)

# Line 6
nodes = len(dist)
with prov.desc("L6 - func call / assign", line=6) as line:
    e_ret = prov.entity("len_dist", repr(nodes), prov.SCRIPT + "eval", "len(dist)", line, attrs=HIDE)
    prov.activity("call", [], [use([e_dist], HIDE)], [e_ret], label="len", attrs=HIDE)
    prov.specializationOf(e_ret, prov.version(e_ret, time(), attrs=SPECIFIC), attrs=SPECIFIC)

    e_nodes = prov.entity("nodes", repr(nodes), prov.SCRIPT + "name", "nodes", line, attrs=HIDE)
    prov.activity("assign", [prov.RefDerivation(time(), e_nodes, e_ret, attrs=HIDE)], attrs=HIDE)


# Line 7
indexes = range(nodes)
with prov.desc("L7 - func call / list assign", line=7) as line:
    ti = time()
    e_ret = prov.entity("range_nodes", repr(list(indexes)), prov.SCRIPT + "eval", "range(nodes)", line)
    e_ret_v = prov.version(e_ret, ti, attrs=SPECIFIC)
    prov.specializationOf(e_ret, e_ret_v, attrs=SPECIFIC)
    e_items = []
    for i in indexes:
        e_item = prov.entity("range_nodes{}".format(i), str(i), prov.SCRIPT + "item", None, line)
        prov.specializationOf(e_item, prov.version(e_item, ti, attrs=SPECIFIC), attrs=SPECIFIC)
        prov.hadDictionaryMember(e_ret_v, e_item, str(i), attrs=SPECIFIC)
    prov.activity("call", [], [e_nodes], [e_ret], label="range", attrs=HIDE)

    e_indexes = prov.entity("indexes", repr(list(indexes)), prov.SCRIPT + "name", "indexes", line)
    prov.activity("assign", [prov.RefDerivation(time(), e_indexes, e_ret, attrs=HIDE)], attrs=HIDE)


# Line 8
for k in indexes:
    with prov.desc("L8 - loop access", line=8) as line:
        e_k = prov.entity("k", k, prov.SCRIPT + "name", "k", line, show1=True, attrs=HIDE)
        item = get_item(e_indexes, k)
        prov.activity("access", [prov.AccessDerivation(time(), e_indexes, str(k), e_k, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

    # Line 9
    distk = dist[k]
    with prov.desc("L9 - access / assign", line=9) as line:
        e_dist_ak = prov.entity("dist@k@", repr(distk), prov.SCRIPT + "access", "dist[k]", line, show1=True)
        item = get_item(e_dist, k)
        prov.activity("access", [prov.AccessDerivation(time(), e_dist, str(k), e_dist_ak, item, attrs=HIDE)], used=[e_dist, e_k], attrs=HIDE)

        e_distk = prov.entity("distk", repr(distk), prov.SCRIPT + "name", "distk", line, show1=True)
        prov.activity("assign", [prov.RefDerivation(time(), e_distk, e_dist_ak, attrs=HIDE)], attrs=HIDE)

    # Line 10
    for i in indexes:
        with prov.desc("L10 - loop access", line=10) as line:
            e_i = prov.entity("i", i, prov.SCRIPT + "name", "i", line, show1=True, attrs=HIDE)
            item = get_item(e_indexes, i)
            prov.activity("access", [prov.AccessDerivation(time(), e_indexes, str(i), e_i, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

        # Line 11
        with prov.desc("L11 - condition", line=11) as line:
            cond([e_i, e_k])

        # Line 12
        disti = dist[i]
        with prov.desc("L12 - access / assign", line=12) as line:
            e_dist_ai = prov.entity("dist@i", repr(disti), prov.SCRIPT + "access", "dist[i]", line, show1=True)
            item = get_item(e_dist, i)
            prov.activity("access", [prov.AccessDerivation(time(), e_dist, str(i), e_dist_ai, item, attrs=HIDE)], used=[e_dist, e_i], attrs=HIDE)

            e_disti = prov.entity("disti", repr(disti), prov.SCRIPT + "name", "disti", line, show1=True)
            prov.activity("assign", [prov.RefDerivation(time(), e_disti, e_dist_ai, attrs=HIDE)], attrs=HIDE)

        # Line 13
        for j in indexes:
            with prov.desc("L13 - loop access", line=13) as line:
                e_j = prov.entity("j", j, prov.SCRIPT + "name", "j", line, attrs=HIDE, show1=True)
                item = get_item(e_indexes, j)
                prov.activity("access", [prov.AccessDerivation(time(), e_indexes, str(j), e_j, item, attrs=HIDE)], used=[e_indexes], attrs=HIDE)

            # Line 14
            with prov.desc("L14 - condition", line=14) as line:
                cond([e_j, e_k, e_i])
            if j == k or j == i: continue

            # Line 15
            ikj = disti[k] + distk[j]
            with prov.desc("L15 - access / access / operation / assign", line=15) as line:
                e_disti_ak = prov.entity("disti@k", repr(disti[k]), prov.SCRIPT + "access", "disti[k]", line, show1=True, attrs=HIDE)
                item = get_item(e_disti, k)
                prov.activity("access", [prov.AccessDerivation(time(), e_disti, str(k), e_disti_ak, item, attrs=HIDE)], used=[e_disti, e_k], attrs=HIDE)

                e_distk_aj = prov.entity("distk@j", repr(distk[j]), prov.SCRIPT + "access", "distk[j]", line, show1=True, attrs=HIDE)
                item = get_item(e_distk, j)
                prov.activity("access", [prov.AccessDerivation(time(), e_distk, str(j), e_distk_aj, item, attrs=HIDE)], used=[e_distk, e_j], attrs=HIDE)

                e_sum = prov.entity("sum", repr(ikj), prov.SCRIPT + "operation", "disti[k] + distk[j]", line, show1=True, attrs=HIDE)
                prov.specializationOf(e_sum, prov.version(e_sum, time(), attrs=SPECIFIC), attrs=SPECIFIC)
                prov.activity("+", [(e_sum, e_disti_ak, e_distk_aj)], attrs=HIDE)

                e_ikj = prov.entity("ikj", repr(ikj), prov.SCRIPT + "name", "ikj", line, show1=True)
                prov.activity("assign", [prov.RefDerivation(time(), e_ikj, e_sum, attrs=HIDE)], attrs=HIDE)

            # Line 16
            with prov.desc("L16 - access", line=16) as line:
                e_disti_aj = prov.entity("disti@j", repr(disti[j]), prov.SCRIPT + "access", "disti[j]", line, show1=True, attrs=HIDE)
                item = get_item(e_disti, j)
                prov.activity("access", [prov.AccessDerivation(time(), e_disti, str(k), e_disti_aj, item, attrs=HIDE)], used=[e_disti, e_j], attrs=HIDE)
                ucond = cond([e_disti_aj, e_ikj])
            if disti[j] > ikj:

                # Line 17
                disti[j] = ikj
                with prov.desc("L17 - part assign with propagation", line=17) as line:
                    derived = []
                    used = [use([e_disti], SPECIFIC), e_j]
                    used += ucond # from if
                    generated = []

                    ti = time()
                    e_disti_aj = prov.entity("disti@j", repr(ikj), prov.SCRIPT + "access", "disti[j]", line, show1=True)
                    follow_ref = prov.SAME[e_disti]
                    follow_value = prov.VALUES[follow_ref]

                    e_disti_v = prov.version(follow_ref, ti, attrs=SPECIFIC)
                    prov.derivedByInsertionFrom(e_disti_v, follow_value, {j: e_disti_aj}, attrs=SPECIFIC)
                    prov.specializationOf(follow_ref, e_disti_v, attrs=SPECIFIC)

                    prov.activity("assign", [prov.WriteDerivation(ti, e_disti, str(j), e_disti_aj, e_ikj)], used=used)



# Line 18
print(result[0][2])
with prov.desc("L18 - access / access / call", line=18) as line:
    e_result_a0 = prov.entity("result@0", repr(result[0]), prov.SCRIPT + "access", "result[0]", line, attrs=HIDE)
    item = get_item(e_result, "0")
    prov.activity("access", [prov.AccessDerivation(time(), e_result, "0", e_result_a0, item, attrs=HIDE)], used=[e_result, e_n0], attrs=HIDE)

    e_result_a02 = prov.entity("result@0@2", repr(result[0][2]), prov.SCRIPT + "access", "result[0][2]", line, attrs=HIDE)
    item = get_item(e_result_a0, "2")
    prov.activity("access", [prov.AccessDerivation(time(), e_result_a0, "2", e_result_a02, item, attrs=HIDE)], used=[e_result_a0, e_n2], attrs=HIDE)

    prov.activity("print", [], [e_result_a02], attrs=HIDE)

prov.finish(show_count=False)
