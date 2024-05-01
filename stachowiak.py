import argparse
from functools import reduce
import itertools
import math
from typing import Tuple

from permutation_graphs import *
from path_operations import *
from verhoeff import HpathNS


def generate_all_di(chain_p: tuple) -> List[list]:
    """" This function corresponds to the start of the proof of Lemma 2 (case 2.1 if |P| even) """
    q = (0, 1)
    d_all = []

    for j in range(len(chain_p) + 1):
        d_i = []
        for i in range(len(chain_p) + 1 - j):
            d_i.append(chain_p[:i] + (q[0],) + chain_p[i + j:] + (q[1],) + chain_p[:j])
        for i in reversed(range(len(chain_p) + 1 - j)):
            d_i.append(chain_p[:i] + (q[1],) + chain_p[i + j:] + (q[0],) + chain_p[:j])
        d_all.append(d_i)
    return d_all


def generate_all_di_prime(chain_p: tuple) -> List[list]:
    """" This function corresponds to the start of the proof of Lemma 2 (case 2.2 if |P| even) """
    q = (0, 1)
    d_all = []

    for j in range(len(chain_p) + 1):
        d_i = []
        for i in range(len(chain_p) + 1 - j):
            d_i.append(chain_p[:i] + (q[1],) + chain_p[i + j:] + (q[0],) + chain_p[:j])
        for i in reversed(range(len(chain_p) + 1 - j)):
            d_i.append(chain_p[:i] + (q[0],) + chain_p[i + j:] + (q[1],) + chain_p[:j])
        d_all.append(d_i)
    return d_all


def lemma2_cycle(chain_p: tuple, case_2_1=True) -> list:
    """"
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


def lemma2_extended_path(chain_p: tuple, case_2_1=True) -> list:
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


def _lemma8_helper(sig_occ: List[Tuple[int, int]]) -> Tuple[List[tuple], List[tuple]]:
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
        for index in range(sig_occ[2][1]+1):
            q.append((first_char, second_char))
            q2.append((second_char, first_char))
            cycle1.append(k_q[index:] + l_p + k_q[:index])
            cycle2.append(k_q[:index] + l_p + k_q[index:])
        cycle1.extend(cycle2)
        q.extend(q2)
        return q, cycle1
    else:
        all_q, result, end_q, end_res = [], [], [], []
        for i in reversed(range(sig_occ[2][1]+1)):
            ge = []
            q, g_i = _lemma8_helper(sig_occ[:2] + [(sig_occ[2][0], sig_occ[2][1]-i)] + [(sig_occ[3][0], sig_occ[3][1]-1)])
            for j, suffix in enumerate(g_i):
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


def _lemma7_constructor(sig: List[int]) -> Tuple[List[tuple], List[tuple]]:
    """
     The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
     We assume sig has the form [1, 1, q, p]
    """
    return _lemma8_helper([(0, 1), (1, 1), (2, sig[2]), (3, sig[3])])


def lemma7(sig: List[int]) -> List[tuple]:
    """
     The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
     We assume sig has the form [1, 1, q, p]
    """
    q, suffix = _lemma7_constructor(sig)
    cycle = [q[i] + suffix[i] for i in range(len(q))]
    assert cycleQ(cycle)
    return cycle


def _lemma8_subgraph_cutter(cyc: List[tuple], x: tuple, y: tuple) -> List[tuple]:
    """
     Makes sure x is the start node of the subgraph and y is the end node
    :param cyc: cycle in a subgraph
    :param x: node that should be at the start of the path
    :param y: node that should be at the end of the path
    :return:
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


def _lemma8_g_i_sub_graphs(k_q, l_p, sig) -> List[List[tuple]]:
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
                l7_q_set, l7_suffix = _lemma8_helper([(0, 1), (3, 1), (2, len(k_q)), (3, i)])
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(l_p[:2 * j] + l7_q_set[l7_i] + l_p[:len(l_p) - i - 2 * j - 1] + (1,) + l7_suffix[l7_i])
                x_ij = l_p[:2 * j] + (0,) + l_p[:len(l_p) - i - 2 * j] + (1,) + l_p[:i] + k_q
                y_ij = l_p[:2 * j + 1] + (0,) + l_p[:len(l_p) - i - 2 * j - 1] + (1,) + l_p[:i] + k_q
            # j == (p-i)/2
            elif j == (len(l_p) - i) / 2:
                l7_subgraph = lemma7(sig[:3] + [i])
                for item in l7_subgraph:
                    g_ij.append(l_p[:len(l_p) - i] + item)
                x_ij = l_p[:len(l_p) - i] + (0, 1) + l_p[:i] + k_q
                y_ij = l_p[:len(l_p) - i] + (1, 0) + l_p[:i] + k_q
            # (p-i)/2 < j <= p-i
            else:
                l7_q_set, l7_suffix = _lemma8_helper([(3, 1), (1, 1), (2, sig[2]), (3, i)])
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(
                        l_p[:2 * (len(l_p) - i - j)] + l7_q_set[l7_i] + l_p[:i + 2 * j - len(l_p) - 1] + (0,) + l7_suffix[
                            l7_i])
                x_ij = l_p[:2 * (len(l_p) - i - j) + 1] + (1,) + l_p[:i + 2 * j - len(l_p) - 1] + (0,) + l_p[:i] + k_q
                y_ij = l_p[:2 * (len(l_p) - i - j)] + (1,) + l_p[:i + 2 * j - len(l_p)] + (0,) + l_p[:i] + k_q
            g_ij = _lemma8_subgraph_cutter(
                g_ij,
                x_ij,
                y_ij
            )
            g_i.extend(g_ij)

        if g_i[0] == ((0,) + l_p[:len(l_p) - i] + (1,) + l_p[:i] + k_q):
            g_all.append(g_i)
        else:
            g_all.append(g_i[::-1])
    return g_all


def _lemma9_g_i_sub_graphs_r0(k_r, k_s, l_p, sig) -> List[List[tuple]]:
    """
    Creates the G_i sub graphs of Lemma 8 (by making the G_ij sub graphs and connecting them)
    :param k_r: chain of r elements "k"
    :param k_s: chain of s elements "k"
    :param l_p: chain of p element "l"
    :param sig: signature of the sequence; form 1,1,r,s,p
    :return: [ G_1, G_2, ... ]
    """
    g_all = []
    for i in range(1, len(l_p) + 1):
        g_i = []
        for j in range(len(l_p) - i + 1):
            g_ij = []
            # O <= j < (p-i)/2
            if j < (len(l_p) - i) / 2:
                l7_q_set, l7_suffix = _lemma8_helper([(0, 1), (3, 1), (2, len(k_s)), (3, i)])
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(k_r + l_p[:2 * j] + l7_q_set[l7_i] + l_p[:len(l_p) - i - 2 * j - 1] + (1,) + l7_suffix[l7_i])
                x_ij = k_r + l_p[:2 * j] + (0,) + l_p[:len(l_p) - i - 2 * j] + (1,) + l_p[:i] + k_s
                y_ij = k_r + l_p[:2 * j + 1] + (0,) + l_p[:len(l_p) - i - 2 * j - 1] + (1,) + l_p[:i] + k_s
            # j == (p-i)/2
            elif j == (len(l_p) - i) / 2:
                l7_subgraph = lemma7(sig[:3] + [i])
                for item in l7_subgraph:
                    g_ij.append(k_r + l_p[:len(l_p) - i] + item)
                x_ij = k_r + l_p[:len(l_p) - i] + (0, 1) + l_p[:i] + k_s
                y_ij = k_r + l_p[:len(l_p) - i] + (1, 0) + l_p[:i] + k_s
            # (p-i)/2 < j <= p-i
            else:
                l7_q_set, l7_suffix = _lemma8_helper([(3, 1), (1, 1), (2, len(k_s)), (3, i)])
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(
                        k_r + l_p[:2 * (len(l_p) - i - j)] + l7_q_set[l7_i] + l_p[:i + 2 * j - len(l_p) - 1] + (0,) + l7_suffix[
                            l7_i])
                x_ij = k_r + l_p[:2 * (len(l_p) - i - j) + 1] + (1,) + l_p[:i + 2 * j - len(l_p) - 1] + (0,) + l_p[:i] + k_s
                y_ij = k_r + l_p[:2 * (len(l_p) - i - j)] + (1,) + l_p[:i + 2 * j - len(l_p)] + (0,) + l_p[:i] + k_s
            g_ij = _lemma8_subgraph_cutter(
                g_ij,
                x_ij,
                y_ij
            )
            g_i.extend(g_ij)

        if g_i[0] == (k_r + (0,) + l_p[:len(l_p) - i] + (1,) + l_p[:i] + k_s):
            g_all.append(g_i)
        else:
            g_all.append(g_i[::-1])
    return g_all


def _lemma9_glue_a_edges(k_r: Tuple[int, ...], k_s: Tuple[int, ...], l_p: Tuple[int, ...], p: int, sub_cycles):
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
            k_r + (0,) + l_p[:p - 1] + (1,) + (k_s[0], l_p[0]) + k_s[1:],
            k_r + (0,) + l_p[:p - 1] + (1, l_p[0]) + k_s,
        )
    else:
        g_result_start = _lemma8_subgraph_cutter(
            sub_cycles[0],
            (0,) + l_p[:p - 1] + (1,) + (k_r[0], l_p[0]) + k_r[1:],
            (0,) + l_p[:p - 1] + (1, l_p[0]) + k_r,
        )
    g_result_end = []
    # for each of the floor((p+1)/2) sub cycles
    for i in range(1, len(sub_cycles)-((p+1) % 2)):
        # take the first a1 and a2 and make them into a cycle from a1 ~ all nodes in cycle ~ a2
        a_2i_1 = k_r + (0,) + l_p[:p - 2 * i] + (1,) + l_p[:2 * i] + k_s
        a_2i_2 = k_r + (0,) + l_p[:p - 2 * i] + (1,) + l_p[:2 * i - 1] + (k_s[0], l_p[0]) + k_s[1:]
        cyc = _lemma8_subgraph_cutter(sub_cycles[i], a_2i_1, a_2i_2)
        # then cut that cycle in 2 by splitting after the next a1 (and thus before the next a2)
        next_a_2 = k_r + (0,) + l_p[:max(p - ((2 * i) + 1), 0)] + (1,) + l_p[:(2 * i) + 1] + k_s
        p1, p2 = splitPathIn2(cyc, next_a_2)
        g_result_start.extend(p1)
        g_result_end.extend(p2[::-1])
    if p % 2 == 0:
        # if p is even, we are still missing the last cycle which we only have to sort from the last a1~nodes~a2
        a_last_1 = k_r + (0, 1) + l_p + k_s
        a_last_2 = k_r + (0, 1) + l_p[:-1] + (k_s[0], l_p[-1]) + k_s[1:]
        g_result_start.extend(_lemma8_subgraph_cutter(sub_cycles[-1], a_last_1, a_last_2))
    g_result_start.extend(g_result_end[::-1])
    return g_result_start


def lemma8(sig: List[int]) -> List[tuple]:
    """
     The graph G=GE( ((0|1) k^q) | l^p) ) contains a Hamilton cycle for every p, q > O.
     We assume sig has the form [1, 1, q, p]
    """
    k_q = tuple([2] * sig[2])
    l_p = tuple([3] * sig[3])
    g_0, g_0_end = [], []
    for i in range(sig[3]+1):
        g_0.append(l_p[:i] + (0,) + l_p[i:] + (1,) + k_q)
        g_0_end.append(l_p[i:] + (1,) + l_p[:i] + (0,) + k_q)
    g_0.extend(g_0_end)
    g_all = [g_0] + _lemma8_g_i_sub_graphs(k_q, l_p, sig)
    sub_cycles = []
    for i in range(0, len(g_all) - (len(g_all) % 2), 2):
        sub_cycles.append(g_all[i] + g_all[i+1][::-1])
    if len(g_all) % 2 == 1:
        sub_cycles.append(g_all[-1])
    g_result_start = _lemma9_glue_a_edges((), k_q, l_p, sig[3], sub_cycles)
    return g_result_start


def lemma9(sig: List[int]) -> List[tuple]:
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
                recursive_lists.append(l_p[:len(l_p)-i] + k_r[:1] + item)
            # a_i = l^{p-i} k l^i k^{r-1} 01 k^s
            ai = l_p[:len(l_p)-i] + k_r[:1] + l_p[:i] + k_r[:len(k_r)-1] + (0, 1) + k_s
            ai_index = recursive_lists.index(ai)
            # l^{p-i} k l^i k^{r-1} 01 k^s
            aj = l_p[:len(l_p)-i] + k_r[:1] + l_p[:i] + k_r[:len(k_r)-1] + (1, 0) + k_s
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


def _lemma10_helper(K: List[tuple], p: int, new_color: int):
    """K is a Hamiltonian path in Q, p is the length of the last part of the signature (l^p)"""
    G = []
    l_p = tuple([new_color] * p)
    for node in K:
        if node == (0, 1, 0, 0, 1, 1):
            print(f"Node: {node} is a part of K")
    for i in range(int(len(K)/2)):
        # Constructing cycles Ci taking graphs 'including' vertices on 2*i and 2*i+1 position
        for j, item in enumerate(K[2 * i]):
            # determining r and s - location of a swap
            if item != K[2 * i + 1][j]:
                r = j
                s = len(K[2 * i]) - r - 2
                break
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
        G.extend([g_modified])  # adding cycle to G

    cycle = []
    # gluing the cycles
    for i, gi in enumerate(G):
        # ai = [p * ['L'] + K[2 * i], (p - 1) * ['L'] + [K[2 * i][0]] + ['L'] + K[2 * i][1:]]
        ai = [l_p + K[2 * i], l_p[:-1] + tuple([K[2 * i][0]]) + l_p[-1:] + K[2 * i][1:]]
        # bi = [K[2 * i] + p * ['L'], K[2 * i][:-1] + ['L'] + [K[2 * i][-1]] + (p - 1) * ['L']]
        bi = [K[2 * i] + l_p, K[2 * i][:-1] + l_p[-1:] + tuple([K[2 * i][-1]]) + l_p[:-1]]
        if i > 0:
            # aj = [p * ['L'] + K[2 * i - 1], (p - 1) * ['L'] + [K[2 * i - 1][0]] + ['L'] + K[2 * i - 1][1:]]
            aj = [l_p + K[2 * i - 1], l_p[:-1] + tuple([K[2 * i - 1][0]]) + l_p[-1:] + K[2 * i - 1][1:]]
            # bj = [K[2 * i - 1] + p * ['L'], K[2 * i - 1][:-1] + ['L'] + [K[2 * i - 1][-1]] + (p - 1) * ['L']]
            bj = [K[2 * i - 1] + l_p, K[2 * i - 1][:-1] + l_p[-1:] + tuple([K[2 * i - 1][-1]]) + l_p[:-1]]
            if adjacent(ai[0], aj[0]) and adjacent(ai[1], aj[1]):
                ind_ai = gi.index(ai[0])
                ind_aj = cycle.index(aj[0])
                # preparing a cycle gi so that ai[0] the first and ai[1] second in list
                if gi[(ind_ai + 1) % (len(gi) - 1)] == ai[1]:
                    gi = gi[ind_ai:] + gi[:ind_ai]
                else:
                    gi.reverse()
                    ind_ai = gi.index(ai[0])
                    gi = gi[ind_ai:] + gi[:ind_ai]
                # preparing the cycle (already glued ones) st aj[0] first and aj[1] last in list
                if ind_aj + 1 == len(cycle):  # if it is last Index error
                    if cycle[0] == aj[1]:
                        cycle.reverse()
                    else:
                        cycle = [cycle[-1]] + cycle[:-1]
                elif cycle[ind_aj + 1] == aj[1]:  # if aj[0], aj[1]
                    cycle = cycle[ind_aj + 1:] + cycle[:ind_aj + 1]
                    cycle.reverse()
                else:  # [aj[1], aj[0]]
                    cycle = cycle[ind_aj:] + cycle[:ind_aj]
            # if ai, aj not parallel we do the same for b
            elif adjacent(bi[0], bj[0]) and adjacent(bi[1], bj[1]):
                ind_bi = gi.index(bi[0])
                ind_bj = cycle.index(bj[0])
                if gi[(ind_bi + 1) % (len(gi) - 1)] == bi[1]:
                    gi = gi[ind_bi:] + gi[:ind_bi]
                else:
                    gi.reverse()
                    ind_bi = gi.index(bi[0])
                    gi = gi[ind_bi:] + gi[:ind_bi]

                if ind_bj + 1 == len(cycle):
                    if cycle[0] == bj[1]:
                        cycle.reverse()
                    else:
                        cycle = [cycle[-1]] + cycle[:-1]
                elif cycle[ind_bj + 1] == bj[1]:  # if aj [0, 1] in order we put a[0] infront, aj[1] at the back
                    cycle = cycle[ind_bj + 1:] + cycle[:ind_bj + 1]
                    cycle.reverse()
                else:
                    cycle = cycle[ind_bj:] + cycle[:ind_bj]
            print(f"cycle {i}/{len(G)} is still a cycle {cycleQ(cycle)}, adjacent start {adjacent(gi[0], cycle[0])} and end {adjacent(gi[1], cycle[-1])}")
            cycle = [gi[0]] + cycle + gi[1:]
        elif i == 0:
            cycle.extend(gi)
    return cycle


def lemma10(sig):
    """If q = |Q| > 2, Q is even and GE(Q) contains a Hamiltonian path and p > 0 then GE(Q|l^p) has a Hamiltonian cycle."""
    K = HpathNS(sig[0], sig[1])
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig):
    """If q = |Q| > 2, p = |P| > 0 and GE(Q) has an even number of vertices and contains a Hamiltonian path then then GE(Q|P) has a Hamiltonian cycle."""
    K = HpathNS(sig[0], sig[1])
    cycle = K
    for ind, new_color in enumerate(sig[2:]):
        color = 2 + ind
        new_cycle = _lemma10_helper(cycle, new_color, color)
        cycle = new_cycle
    return cycle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper tool to find paths through permutation neighbor swap graphs.")
    parser.add_argument("-s", "--signature"
                        , type=str, help="Input permutation signature (comma separated)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args()
    s = [int(x) for x in args.signature.split(",")]
    if len(s) > 1:
        if len(s) == 2:
            perms_odd = HpathNS(s[0], s[1])
            print(f"Both {s[0]} and {s[1]} are odd: {len(set(perms_odd))}/{len(perms_odd)}/{math.comb(s[0] + s[1], s[1])}")
            print(perms_odd, pathQ(perms_odd), cycleQ(perms_odd))
        elif s[0] % 2 == 0 or s[1] % 2 == 0:
            raise ValueError("The first two elements of the signature should be odd for Stachowiak's permutations")
        l11 = lemma11(s)
        print(f"lemma 11 results {l11}")
        print(f"lemma 11 {len(set(l11))}/{len(l11)}/{multinomial(s)} is a path: {pathQ(l11)} and a cycle: {cycleQ(l11)}")