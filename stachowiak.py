import argparse
import itertools
import math

from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    cycleQ,
    pathQ,
    splitPathIn2,
)
from helper_operations.permutation_graphs import multinomial
from steinhaus_johnson_trotter import SteinhausJohnsonTrotter
from verhoeff import HpathNS


def generate_all_di(chain_p: tuple) -> list[list[int]]:
    """This function corresponds to the start of the proof of Lemma 2 (case 2.1 if |P| even)"""
    q = (0, 1)
    d_all = []

    for j in range(len(chain_p) + 1):
        d_i = []
        for i in range(len(chain_p) + 1 - j):
            d_i.append(chain_p[:i] + (q[0],) + chain_p[i + j :] + (q[1],) + chain_p[:j])
        for i in reversed(range(len(chain_p) + 1 - j)):
            d_i.append(chain_p[:i] + (q[1],) + chain_p[i + j :] + (q[0],) + chain_p[:j])
        d_all.append(d_i)
    return d_all


def generate_all_di_prime(chain_p: tuple) -> list[list[int]]:
    """This function corresponds to the start of the proof of Lemma 2 (case 2.2 if |P| even)"""
    q = (0, 1)
    d_all = []

    for j in range(len(chain_p) + 1):
        d_i = []
        for i in range(len(chain_p) + 1 - j):
            d_i.append(chain_p[:i] + (q[1],) + chain_p[i + j :] + (q[0],) + chain_p[:j])
        for i in reversed(range(len(chain_p) + 1 - j)):
            d_i.append(chain_p[:i] + (q[0],) + chain_p[i + j :] + (q[1],) + chain_p[:j])
        d_all.append(d_i)
    return d_all


def lemma2_cycle(chain_p: tuple, case_2_1=True) -> list[tuple[int, ...]]:
    """
    This function generates the cycles of Lemma 2.
    If |P| is even the last two nodes are discarded as in the Lemma.
    Defaults to case 2.1 of Lemma 2. If the case_2_1 variable is set to false, the cycle will be as in case 2.2
    """
    if case_2_1:
        d_all = generate_all_di(chain_p)
    else:
        d_all = generate_all_di_prime(chain_p)
    chain_1_1_path, last_elements = [], []
    for index, d_i in enumerate(d_all):
        # in case the |P| is even, don't add the elements 01l^p and 10l^p
        if index == len(d_all) - 1 and len(d_all) % 2 == 1:
            continue
        # never add the last elements, those will be added at the end to create a cycle
        if index % 2 == 0:
            # add the reversed list without the last element
            chain_1_1_path.append(d_i[-2::-1])
        else:
            chain_1_1_path.append(d_i[:-1])
        # keep track of the last elements
        last_elements.append(d_i[-1])
    # add the last elements of every d_i to complete the cycle
    cycle = list(itertools.chain(*([last_elements[::-1]] + chain_1_1_path)))
    assert cycleQ(cycle)
    return cycle


def lemma2_extended_path(chain_p: tuple, case_2_1=True) -> list[tuple[int, ...]]:
    """
    Extends the cycle of Lemma 2 with the last two elements in case |P| is even
    if |P| odd the cycle is returned
    Defaults to case 2.1 of Lemma 2. If the case_2_1 variable is set to false, the path will be as in case 2.2
    """
    cycle = lemma2_cycle(chain_p, case_2_1)
    if len(chain_p) % 2 == 0:
        if case_2_1:
            path = [(0, 1) + chain_p, (1, 0) + chain_p] + cycle
        else:
            path = [(1, 0) + chain_p, (0, 1) + chain_p] + cycle
        assert pathQ(path)
        return path
    return cycle


def _lemma8_helper(
    sig_occ: list[tuple[int, int]]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
    We assume sig_occ has the form [(char, 1), (char, 1), (char, q), (char, p)]
    """
    first_char = sig_occ[0][0]
    second_char = sig_occ[1][0]
    assert sig_occ[0][1] == 1
    assert sig_occ[1][1] == 1
    assert first_char != second_char
    assert sig_occ[2][0] != sig_occ[3][0]
    k_q = tuple([sig_occ[2][0]] * sig_occ[2][1])
    l_p = tuple([sig_occ[3][0]] * sig_occ[3][1])
    if sig_occ[3][1] == 1:
        q, q2, cycle1, cycle2 = [], [], [], []
        for index in range(sig_occ[2][1] + 1):
            q.append((first_char, second_char))
            q2.append((second_char, first_char))
            cycle1.append(k_q[index:] + l_p + k_q[:index])
            cycle2.append(k_q[:index] + l_p + k_q[index:])
        cycle1.extend(cycle2)
        q.extend(q2)
        return q, cycle1
    else:
        all_q, result, end_q, end_res = [], [], [], []
        for i in reversed(range(sig_occ[2][1] + 1)):
            ge = []
            q, g_i = _lemma8_helper(
                sig_occ[:2]
                + [(sig_occ[2][0], sig_occ[2][1] - i)]
                + [(sig_occ[3][0], sig_occ[3][1] - 1)]
            )
            for suffix in g_i:
                node = k_q[:i] + (l_p[0],) + suffix
                ge.append(node)
            if i % 2 != sig_occ[2][1] % 2:
                all_q.extend(q[:0:-1])
                result.extend(ge[:0:-1])
            else:
                all_q.extend(q[1:])
                result.extend(ge[1:])
            end_q.append(q[0])
            end_res.append(ge[0])
        all_q.extend(end_q[::-1])
        result.extend(end_res[::-1])
        return all_q, result


def _lemma7_constructor(
    sig: list[int],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
    We assume sig has the form [1, 1, q, p]
    """
    return _lemma8_helper([(0, 1), (1, 1), (2, sig[2]), (3, sig[3])])


def lemma7(sig: list[int]) -> list[tuple[int, ...]]:
    """
    The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
    We assume sig has the form [1, 1, q, p]
    """
    q, suffix = _lemma7_constructor(sig)
    cycle = [q[i] + suffix[i] for i in range(len(q))]
    assert cycleQ(cycle)
    return cycle


def _lemma8_subgraph_cutter(
    cyc: list[tuple], x: tuple, y: tuple
) -> list[tuple[int, ...]]:
    """
     Makes sure x is the start node of the subgraph and y is the end node
    :param cyc: cycle in a subgraph
    :param x: node that should be at the start of the path
    :param y: node that should be at the end of the path
    :return: subgraph with x as start and y as end
    """
    try:
        assert adjacent(x, y)
    except AssertionError as err:
        print(f"{repr(err)} not adjacent for x: {x}, y: {y}")
        quit()
    try:
        assert cycleQ(cyc)
    except AssertionError as err:
        print(f"{repr(err)} not a cycle: {cyc}")
        quit()
    try:
        assert x in cyc and y in cyc
    except AssertionError as err:
        print(f"{repr(err)} for x: {x}, y: {y}, not in cycle: {cyc}")
        quit()
    cyc_cut = cutCycle(cyc, x)
    if cyc_cut[1] == y:
        res = (cyc_cut[1:] + cyc_cut[:1])[::-1]
        assert cycleQ(res)
        return res
    assert cycleQ(cyc_cut)
    return cyc_cut


def _lemma8_g_i_sub_graphs(
    k_q: tuple[int, ...], l_p: tuple[int, ...], sig: list[int]
) -> list[list[tuple]]:
    """
    Creates the G_i sub graphs of Lemma 8 (by making the G_ij sub graphs and connecting them)
    :param k_q: chain of q elements "k"
    :param l_p: chain of p element "l"
    :param sig: signature of the sequence; form 1,1,q,p
    :return: [ G_1, G_2, ... ]
    """
    g_all = []
    for i in range(1, len(l_p) + 1):
        g_i = []
        for j in range(len(l_p) - i + 1):
            g_ij = []
            # O <= j < (p-i)/2
            if j < (len(l_p) - i) / 2:
                l7_q_set, l7_suffix = _lemma8_helper(
                    [(0, 1), (3, 1), (2, len(k_q)), (3, i)]
                )
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(
                        l_p[: 2 * j]
                        + l7_q_set[l7_i]
                        + l_p[: len(l_p) - i - 2 * j - 1]
                        + (1,)
                        + l7_suffix[l7_i]
                    )
                x_ij = (
                    l_p[: 2 * j]
                    + (0,)
                    + l_p[: len(l_p) - i - 2 * j]
                    + (1,)
                    + l_p[:i]
                    + k_q
                )
                y_ij = (
                    l_p[: 2 * j + 1]
                    + (0,)
                    + l_p[: len(l_p) - i - 2 * j - 1]
                    + (1,)
                    + l_p[:i]
                    + k_q
                )
            # j == (p-i)/2
            elif j == (len(l_p) - i) / 2:
                l7_subgraph = lemma7(sig[:3] + [i])
                for item in l7_subgraph:
                    g_ij.append(l_p[: len(l_p) - i] + item)
                x_ij = l_p[: len(l_p) - i] + (0, 1) + l_p[:i] + k_q
                y_ij = l_p[: len(l_p) - i] + (1, 0) + l_p[:i] + k_q
            # (p-i)/2 < j <= p-i
            else:
                l7_q_set, l7_suffix = _lemma8_helper(
                    [(3, 1), (1, 1), (2, sig[2]), (3, i)]
                )
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(
                        l_p[: 2 * (len(l_p) - i - j)]
                        + l7_q_set[l7_i]
                        + l_p[: i + 2 * j - len(l_p) - 1]
                        + (0,)
                        + l7_suffix[l7_i]
                    )
                x_ij = (
                    l_p[: 2 * (len(l_p) - i - j) + 1]
                    + (1,)
                    + l_p[: i + 2 * j - len(l_p) - 1]
                    + (0,)
                    + l_p[:i]
                    + k_q
                )
                y_ij = (
                    l_p[: 2 * (len(l_p) - i - j)]
                    + (1,)
                    + l_p[: i + 2 * j - len(l_p)]
                    + (0,)
                    + l_p[:i]
                    + k_q
                )
            g_ij = _lemma8_subgraph_cutter(g_ij, x_ij, y_ij)
            g_i.extend(g_ij)

        if g_i[0] == ((0,) + l_p[: len(l_p) - i] + (1,) + l_p[:i] + k_q):
            g_all.append(g_i)
        else:
            g_all.append(g_i[::-1])
    return g_all


def _lemma9_glue_a_edges(
    k_r: tuple[int, ...],
    k_s: tuple[int, ...],
    l_p: tuple[int, ...],
    p: int,
    sub_cycles: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """
    Glues the a_i edges from Lemma8 together to create the final cycle
    :param k_r: chain of r elements "k"
    :param k_s: chain of s elements "k"
    :param l_p: chain of p element "l"
    :param p: number of l elements (sig[3])
    :param sub_cycles: sub cycles created by gluing y_ij, y_ij+1
    :return: Cycle of all sub cycles glued together
    """
    # make the a1 path, we have as first part of the cycle a11~path~a12
    if len(l_p) == 0:
        return [item for row in sub_cycles for item in row]
    if len(k_s) > 0:
        g_result_start = _lemma8_subgraph_cutter(
            sub_cycles[0],
            k_r + (0,) + l_p[: p - 1] + (1,) + (k_s[0], l_p[0]) + k_s[1:],
            k_r + (0,) + l_p[: p - 1] + (1, l_p[0]) + k_s,
        )
    else:
        g_result_start = _lemma8_subgraph_cutter(
            sub_cycles[0],
            (0,) + l_p[: p - 1] + (1,) + (k_r[0], l_p[0]) + k_r[1:],
            (0,) + l_p[: p - 1] + (1, l_p[0]) + k_r,
        )
    g_result_end = []
    # for each of the floor((p+1)/2) sub cycles
    for i in range(1, len(sub_cycles) - ((p + 1) % 2)):
        # take the first a1 and a2 and make them into a cycle from a1 ~ all nodes in cycle ~ a2
        a_2i_1 = k_r + (0,) + l_p[: p - 2 * i] + (1,) + l_p[: 2 * i] + k_s
        a_2i_2 = (
            k_r
            + (0,)
            + l_p[: p - 2 * i]
            + (1,)
            + l_p[: 2 * i - 1]
            + (k_s[0], l_p[0])
            + k_s[1:]
        )
        cyc = _lemma8_subgraph_cutter(sub_cycles[i], a_2i_1, a_2i_2)
        # then cut that cycle in 2 by splitting after the next a1 (and thus before the next a2)
        next_a_2 = (
            k_r
            + (0,)
            + l_p[: max(p - ((2 * i) + 1), 0)]
            + (1,)
            + l_p[: (2 * i) + 1]
            + k_s
        )
        p1, p2 = splitPathIn2(cyc, next_a_2)
        g_result_start.extend(p1)
        g_result_end.extend(p2[::-1])
    if p % 2 == 0:
        # if p is even, we are still missing the last cycle which we only have to sort from the last a1~nodes~a2
        a_last_1 = k_r + (0, 1) + l_p + k_s
        a_last_2 = k_r + (0, 1) + l_p[:-1] + (k_s[0], l_p[-1]) + k_s[1:]
        g_result_start.extend(
            _lemma8_subgraph_cutter(sub_cycles[-1], a_last_1, a_last_2)
        )
    g_result_start.extend(g_result_end[::-1])
    return g_result_start


def lemma8(sig: list[int]) -> list[tuple[int, ...]]:
    """
    The graph G=GE( ((0|1) k^q) | l^p) ) contains a Hamilton cycle for every p, q > O.
    We assume sig has the form [1, 1, q, p]
    """
    k_q = tuple([2] * sig[2])
    l_p = tuple([3] * sig[3])
    g_0, g_0_end = [], []
    for i in range(sig[3] + 1):
        g_0.append(l_p[:i] + (0,) + l_p[i:] + (1,) + k_q)
        g_0_end.append(l_p[i:] + (1,) + l_p[:i] + (0,) + k_q)
    g_0.extend(g_0_end)
    if sig[3] == 0:
        return g_0
    g_all = [g_0] + _lemma8_g_i_sub_graphs(k_q, l_p, sig)
    sub_cycles = []
    for i in range(0, len(g_all) - (len(g_all) % 2), 2):
        sub_cycles.append(g_all[i] + g_all[i + 1][::-1])
    if len(g_all) % 2 == 1:
        sub_cycles.append(g_all[-1])
    g_result_start = _lemma9_glue_a_edges((), k_q, l_p, sig[3], sub_cycles)
    return g_result_start


def lemma9(sig: list[int]) -> list[tuple[int, ...]]:
    """
    The graph G=GE( (k^r (0|1) k^s) | l^p) ) contains a Hamilton cycle for every p, r+s > O.
    We assume sig has the form [1, 1, r, s, p]
    """
    k_r = tuple([2] * sig[2])
    k_s = tuple([2] * sig[3])
    l_p = tuple([3] * sig[4])
    # if s == 0
    if sig[2] == 0:
        return lemma8(sig[:2] + sig[3:])
    # if r == 0
    if sig[3] == 0:
        # reverse every individual item before returning it
        return [x[::-1] for x in lemma8(sig[:3] + sig[4:])]
    else:
        # r > 0
        G = []
        for i in range(len(l_p) + 1):
            # induction on r, for every 0 \leq i \leq p
            g = lemma9(sig[:2] + [sig[2] - 1, sig[3], i])
            recursive_lists = []
            for item in g:
                recursive_lists.append(l_p[: len(l_p) - i] + k_r[:1] + item)
            # a_i = l^{p-i} k l^i k^{r-1} 01 k^s
            ai = (
                l_p[: len(l_p) - i]
                + k_r[:1]
                + l_p[:i]
                + k_r[: len(k_r) - 1]
                + (0, 1)
                + k_s
            )
            ai_index = recursive_lists.index(ai)
            # l^{p-i} k l^i k^{r-1} 01 k^s
            aj = (
                l_p[: len(l_p) - i]
                + k_r[:1]
                + l_p[:i]
                + k_r[: len(k_r) - 1]
                + (1, 0)
                + k_s
            )
            aj_index = recursive_lists.index(aj)

            # fix the orientation of the list
            if ai_index > aj_index:
                recursive_lists.reverse()
                ai_index = recursive_lists.index(ai)
            recursive_lists = recursive_lists[ai_index:] + recursive_lists[:ai_index]
            G.append(recursive_lists)

        cycle = []
        for i, item in enumerate(G):
            if i == 0:
                cycle.extend(item)
            elif i == 1:
                # this will be the first three nodes of the path: (connecting G_0 and G_1)
                # [l^{p-1} k l k^{r-1} 01 k^s, l^p k^r 01 k^s, l^p k^r 10 k^s, l^{p-1} k l k^{r-1} 10 k^s]
                cycle[0:0] = [item[0]]
                cycle.extend(item[1:])
            # now glue b1 and b2, b3 and b4 etc. and glue a2 and a3, a4 and a5 etc.
            elif i % 2 == 0:
                item.reverse()
                cycle = [item[-1]] + cycle + item[:-1]
            else:
                cycle = [item[0]] + cycle + item[1:]
        return cycle


def _lemma10_subcycle_cutter(
    cycle: list[tuple[int, ...]],
    gi: list[tuple[int, ...]],
    edge_i: tuple[int, ...],
    edge_j: tuple[int, ...],
) -> list[tuple[int, ...]]:
    """
    Cuts the cycle and gi to change them for lemma 10
    :param cycle: cycle to cut for lemma 10
    :param gi: subgraph to cut for lemma 10
    :param edge_i: edge that should be at the start of gi
    :param edge_j: edge that should be the point at which the cycle is cut (see return)
    :return: cycle starts with edge_i[0] and edge_i[1] is the second node
             gi starts with edge_j[0] and edge_j[1] is the last node
    """
    ind_node_i = gi.index(edge_i[0])
    # preparing gi so that node_i[0] the first and node_i[1] second in list
    if gi[(ind_node_i + 1) % (len(gi) - 1)] == edge_i[1]:
        gi = gi[ind_node_i:] + gi[:ind_node_i]
    else:
        gi.reverse()
        ind_node_i = gi.index(edge_i[0])
        gi = gi[ind_node_i:] + gi[:ind_node_i]

    ind_node_j = cycle.index(edge_j[0])
    # preparing the cycle (already glued ones) such that node_j[0] first and node_j[1] last in list
    if ind_node_j + 1 == len(cycle):
        # if cycle ends with node_j[0] and ends with node_j[1]
        if cycle[0] == edge_j[1]:
            cycle.reverse()
        # if cycle ends with node_j[0] and node_j[1] is the second to last element (since they are always neighbors in the path)
        else:
            # move node_j[0] to the start and append the rest of the cycle
            cycle = [cycle[-1]] + cycle[:-1]
    elif cycle[ind_node_j + 1] == edge_j[1]:
        # if node_j[1] is the second element in the cycle
        # change cycle to start with node_j[1] and then append the part until node_j[0]. Then reverse the whole cycle
        cycle = cycle[ind_node_j + 1 :] + cycle[: ind_node_j + 1]
        cycle.reverse()
    else:
        # otherwise we have [node_j[1], node_j[0], ...] so we move node_j[0] to the start and append the part until node_j[1]
        cycle = cycle[ind_node_j:] + cycle[:ind_node_j]
    return cycle, gi


def _lemma10_helper(K: list[tuple], p: int, new_color: int) -> list[tuple[int, ...]]:
    """
    :param K: Hamiltonian path in Q ([K_1, K_2, ..., K_2n])
    :param p: is the length of the last part of the signature (l^p)
    :param new_color: is the new color to add to the graph
    :return Hamiltonian path over Q | l^p
    """
    # G_i = GE(K_{2i-1} | l^p, K_{2i} | l^p) for 0 <= i <= n
    G = []
    l_p = tuple([new_color] * p)
    for i in range(len(K) // 2):
        # Constructing cycles Ci taking graphs 'including' vertices on 2*i and 2*i+1 position
        for j, item in enumerate(K[2 * i]):
            # determining r and s - location of a swap
            if item != K[2 * i + 1][j]:
                r = j
                s = len(K[2 * i]) - r - 2
                break
        # G_i is isomorphic to GE( (k^r (0|1) k^s) | l^p )
        g = lemma9([1, 1, r, s, p])

        g_modified = []
        remove_color = 3
        for item in g:
            new_item = list(item)  # Convert item to a list
            # smartly renaming permutations -> isomorphism, depending on order of 01/10 -
            # tells us either to use 2*2 or 2*i+1
            if new_item.index(0) < new_item.index(1):
                k = 0
                for j, it in enumerate(new_item):
                    if it != remove_color:
                        new_item[j] = K[2 * i][k]
                        k += 1
                    if it == remove_color:
                        new_item[j] = new_color
            else:
                k = 0
                for j, it in enumerate(new_item):
                    if it != remove_color:
                        new_item[j] = K[2 * i + 1][k]
                        k += 1
                    if it == remove_color:
                        new_item[j] = new_color
            g_modified.append(tuple(new_item))  # Convert item back to a tuple
        G.append(g_modified)  # adding cycle to the list of G_i's

    cycle = G[0]
    # K_j = k_{j,1} k_{j,2} \dots k_{j,q}
    for i, gi in enumerate(G[1:], start=1):
        # a_i = (l^p k_{2i}, l^{p-1} k_{2i,1} l k{2i,2} \dots k_{2i,q})
        ai = [l_p + K[2 * i], l_p[:-1] + tuple([K[2 * i][0]]) + l_p[-1:] + K[2 * i][1:]]
        # b_i = (k_{2i} l^p, k_{2i,1} \dots k_{2i,q-1} l k_{2i,q} l^{p-1})
        bi = [
            K[2 * i] + l_p,
            K[2 * i][:-1] + l_p[-1:] + tuple([K[2 * i][-1]]) + l_p[:-1],
        ]
        # a_j = (l^p k_{2i-1}, l^{p-1} k_{2i-1,1} l k_{2i-1,2} \dots, k_{2i-1,q})
        aj = [
            l_p + K[2 * i - 1],
            l_p[:-1] + tuple([K[2 * i - 1][0]]) + l_p[-1:] + K[2 * i - 1][1:],
        ]
        # b_j = (k_{2i-1} l^p, k_{2i-1,1} \dots k_{2i-1,q-1} l k_{2i-1,q} l^{p-1})
        bj = [
            K[2 * i - 1] + l_p,
            K[2 * i - 1][:-1] + l_p[-1:] + tuple([K[2 * i - 1][-1]]) + l_p[:-1],
        ]
        # if K_j and K_{j+1} differ in the first pair of elements, a_j and a_{j+1} are parallel
        if adjacent(ai[0], aj[0]) and adjacent(ai[1], aj[1]):
            cycle, gi = _lemma10_subcycle_cutter(cycle, gi, ai, aj)
        # if K_j and K_{j+1} don't differ in the first pair of elements, b_j and b_{j+1} are parallel
        elif adjacent(bi[0], bj[0]) and adjacent(bi[1], bj[1]):
            cycle, gi = _lemma10_subcycle_cutter(cycle, gi, bi, bj)
        cycle = [gi[0]] + cycle + gi[1:]
    return cycle


def lemma10(sig: list[int]) -> list[tuple[int, ...]]:
    """If q = |Q| > 2, Q is even and GE(Q) contains a Hamiltonian path and p > 0 then GE(Q|l^p) has a Hamiltonian cycle."""
    K = HpathNS(sig[0], sig[1])
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig: list[int]) -> list[tuple[int, ...]]:
    """If q = |Q| > 2, p = |P| > 0 and GE(Q) has an even number of vertices and contains a Hamiltonian path then GE(Q|P) has a Hamiltonian cycle."""
    if len(sig) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(sig) == 1:
        return [(0,) * sig[0]]
    elif sum(sig[:2]) > 2:
        path = HpathNS(sig[0], sig[1])  # K in the paper
        next_color = 2
    elif sig[2] == 1:
        # use the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle if the first 3 (or more) elements are 1
        try:
            next_color = sig.index(next(x for x in sig if x != 1))
        except StopIteration:
            next_color = len(sig)  # all elements are 1
        path = SteinhausJohnsonTrotter.get_sjt_permutations(
            SteinhausJohnsonTrotter(), next_color
        )
    elif sig[2] != 0:
        # use Stachowiak's lemma 2 to find a Hamiltonian path in GE(Q|P[1])
        path = lemma2_extended_path(tuple([2] * sig[2]))
        next_color = 3
    else:
        raise ValueError(
            "q = |Q| > 2 and GE(Q) has an even number of vertices is required for Lemma 11"
        )
    for ind, new_color in enumerate(sig[next_color:], start=next_color):
        cycle = _lemma10_helper(path, new_color, ind)
        path = cycle
    return path


def get_inversion_count(arr, n):
    inv_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inv_count += 1

    return inv_count


def get_parity_counts(sig: list[int]) -> tuple[int, int]:
    """
    Get the parity counts of the signature
    :param sig: signature of the permutation
    :return: tuple of the parity counts (even, odd)
    """
    initial_perm = []
    for idx, count in enumerate(sig):
        initial_perm.extend([idx] * count)
    perms = list(set(list(itertools.permutations(initial_perm))))
    even_count, odd_count = 0, 0
    for perm in perms:
        inv_count = get_inversion_count(perm, len(perm))
        if inv_count % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    return even_count, odd_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Helper tool to find paths through permutation neighbor swap graphs."
    )
    parser.add_argument(
        "-s",
        "--signature",
        type=str,
        help="Input permutation signature (comma separated)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    parser.add_argument(
        "-p",
        "--parities",
        action="store_true",
        help="Show the even and odd counts of all permutations",
    )

    args = parser.parse_args()
    s = [int(x) for x in args.signature.split(",")]
    if args.parities:
        even, odd = get_parity_counts(s)
        print(f"Even: {even}, Odd: {odd} -> diff={abs(even-odd)} for n={sum(s)}")
        if sum(s) % 2 == 0 and abs(even - odd) > 0:
            print(
                f"NO HAMILTONIAN CYCLE POSSIBLE: n={sum(s)} EVEN and diff={abs(even-odd)} != 0"
            )
        elif sum(s) % 2 == 1 and abs(even - odd) != 1:
            print(
                f"NO HAMILTONIAN CYCLE POSSIBLE: n={sum(s)} ODD and diff={abs(even-odd)} != 1"
            )
    if len(s) > 1:
        if len(s) == 2:
            perms_odd = HpathNS(s[0], s[1])
            if args.verbose:
                print(f"Resulting path {perms_odd}")
            print(
                f"Verhoeff's result for k0={s[0]} and k1={s[1]}: {len(set(perms_odd))}/{len(perms_odd)}/{math.comb(s[0] + s[1], s[1])} "
                f"is a path: {pathQ(perms_odd)} and a cycle: {cycleQ(perms_odd)}"
            )
        elif s[0] % 2 == 0 or s[1] % 2 == 0:
            raise ValueError(
                "The first two elements of the signature should be odd for Stachowiak's permutations"
            )
        else:
            l11 = lemma11(s)
            if args.verbose:
                print(f"lemma 11 results {l11}")
            print(
                f"lemma 11 {len(set(l11))}/{len(l11)}/{multinomial(s)} is a path: {pathQ(l11)} and a cycle: {cycleQ(l11)}"
            )
