import argparse
import collections
import copy
import itertools
import math
import sys
from typing import Tuple, Union

from permutation_graphs import *
from path_operations import *
from rivertz import SetPerm


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



def HpathNS(k0: int, k1: int) -> list:
    odd_perms = []
    tuple_0 = tuple(k0 * [0])
    tuple_1 = tuple(k1 * [1])
    sys.setrecursionlimit(2500)
    if k0 == 0:
        if k1 % 2 == 0:
            return []
        return [tuple_1]
    elif k1 == 0:
        if k0 % 2 == 0:
            return []
        return [tuple_0]
    elif k0 == 1:
        # path from 0^k0 1 to 1 0^k0, if k1 odd, else from 0^(k0-1) 1 0 to 1 0^k0
        for i in reversed(range(k1 + 1)):
            odd_perms.append(tuple_1[:i] + tuple_0 + tuple_1[i:])
        return odd_perms[::-1]
    elif k1 == 1:
        # path from 1^k1 0 to 0 1^k1, if k0 odd, else from 1^(k1-1) 0 1 to 0 1^k1
        for i in reversed(range(k0 + 1)):
            odd_perms.append(tuple_0[:i] + tuple_1 + tuple_0[i:])
        return odd_perms[::-1] if k0 % 2 else odd_perms[1:]
    if k0 > k1:
        return [tuple(1 if x == 0 else 0 for x in tup) for tup in HpathNS(k1, k0)]
    if k0 % 2 == 1 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), (1,))  # A Hamiltonian path from 0^k0 1^k1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))  # A Hamiltonian cycle from 1^(k1-1) 0^(k0-1) 1 0

        return p1[:-1] + [p0[-1]] + p0[:-1]

    elif k0 % 2 == 0 and k1 % 2 == 1:
        p1 = extend(HpathNS(k0, k1 - 1), (1,))  # A Hamiltonian cycle containing edge 0^(k0-1) 1^(k1-1) 0 1 ~ 0^(k0-2) 1 0 1^(k1-2) 0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))  # A Hamiltonian path from 0^(k0-1) 1^k1 0 to 1^k1 0^k1
        v = p0[0]

        return [v] + cutCycle(p1[::-1], swapPair(v, -2)) + p0[1:]
    elif k0 % 2 == 0 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), (1,))  # A Hamiltonian path from 0^(k0-1) 1^(k1-1) 0 1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))

        print(f"p's even {k0}, {k1}: p1 {p1[::-1]}, p0 {p0}")
        return p1[::-1] + p0[:-1]
    else:
        p11 = HpathNS(k0, k1 - 2)
        p1101 = HpathNS(k0 - 1, k1 - 3)
        p0101 = HpathNS(k0 - 2, k1 - 2)
        p0001 = HpathNS(k0 - 3, k1 - 1)
        p00 = HpathNS(k0 - 2, k1)

        sp00 = extend(stutterPermutations([k0 - 3, k1 - 1]), (0, 0))
        sp11 = extend(stutterPermutations([k0 - 1, k1 - 3]), (1, 1))
        print(f"p's odd {k0}, {k1}: p11 {p11}, p1101 {p1101}, p0101 {p0101}, p0001 {p0001}, p00 {p00}")
        print("stutter permutations:", sp00, sp11)

        if len(p1101) == 0:
            c11xy = [stut+suff for suff in [(0, 1), (1, 0)] for stut in sp11]
            print("p1101 is 0 gives", c11xy, "between", createSquareTube(p0101[::-1], (0, 1), (1, 0))[-4:-2], "and", createSquareTube(p0101[::-1], (0, 1), (1, 0))[-2:])
        else:
            print("1", p1101, p0101, p0101[0][:-1] + (0,))
            ext_path = extend(cutCycle(p1101, p0101[0][:-1] + (0,)), (1, 1))
            print("ext1", ext_path, "gives", createZigZagPath(ext_path, (0, 1), (1, 0)), "between", createSquareTube(p0101[::-1], (0, 1), (1, 0))[-4:-2], "and", createSquareTube(p0101[::-1], (0, 1), (1, 0))[-2:])
            p11xy = rotate(createZigZagPath(ext_path, (0, 1), (1, 0)), 1)
            print(f"p11xy: {p11xy}, {pathQ(p11xy)}")
            c11xy = incorporateSpursInZigZag(p11xy, sp11)[::-1]
            print(f"p11xy: {p11xy}, len: {len(p11xy)}, c11xy: {c11xy}, len: {len(c11xy)}, {pathQ(c11xy)}, {cycleQ(c11xy)}")

        if len(p0001) == 0:
            c00xy = [stut+suff for suff in [(1, 0), (0, 1)] for stut in sp00]
            print("p0001 is 0 gives", c00xy, "between", createSquareTube(p0101[::-1], (0, 1), (1, 0))[1:3], "and", createSquareTube(p0101[::-1], (0, 1), (1, 0))[3:5])
        else:
            print("2", p0001, p0101, p0101[-1][:-1])
            ext_path = extend(cutCycle(p0001, p0101[-1][:-1] + (1,)), (0, 0))
            print("ext2", ext_path, "gives", createZigZagPath(ext_path, (0, 1), (1, 0)), "between", createSquareTube(p0101[::-1], (0, 1), (1, 0))[:3], "and", createSquareTube(p0101[::-1], (0, 1), (1, 0))[3:5])
            p00xy = rotate(createZigZagPath(ext_path, (0, 1), (1, 0)), 1)
            print(f"p00xy: {p00xy}, {pathQ(p00xy)}")
            c00xy = incorporateSpursInZigZag(p00xy, sp00)

        if k0 != k1 and k0 != 3:
            p00 = p00[::-1]
        if k1 == k0:
            p11 = p11[::-1]

        tube = createSquareTube(p0101[::-1], (0, 1), (1, 0))
        tube1, tube2, tube3 = tube[:3], tube[3:-2], tube[-2:]
        print(
            "p11", len(extend(p11, (1, 1))),
            "+tube1", len(extend(p11, (1, 1)) + tube1),
            "+c00xy", len(extend(p11, (1, 1)) + tube1 + c00xy),
            "+tube2", len(extend(p11, (1, 1)) + tube1 + c00xy + tube2),
            "+c11xy", len(extend(p11, (1, 1)) + tube1 + c00xy + tube2 + c11xy),
            "+tube3", len(extend(p11, (1, 1)) + tube1 + c00xy + tube2 + c11xy + tube3),
        )

        path_ham = extend(p11, (1, 1)) + tube1 + c00xy + tube2 + c11xy + tube3 + extend(p00, (0, 0))
        if len(path_ham) != len(set(path_ham)):
            print("Path contains duplicates:", [item for item, count in collections.Counter(path_ham).items() if count > 1])
        if len(path_ham) < math.comb(k0 + k1, k1):
            rivertz_perms = []
            for p in SetPerm([k0, k1]):
                rivertz_perms.append(p)
            corrected_tuples = [tuple([x - 1 for x in item]) for item in rivertz_perms]
            print("Path is missing elements:", [item for item in corrected_tuples if item not in path_ham])
        return path_ham


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper tool to find paths through permutation neighbor swap graphs.")
    parser.add_argument("-s", "--signature"
                        , type=str, help="Input permutation signature (comma separated)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args()
    s = [int(x) for x in args.signature.split(",")]
    if len(s) > 1:
        if s[0] % 2 == 0 or s[1] % 2 == 0:
            raise ValueError("The first two elements of the signature should be odd for Stachowiak's permutations")
        if len(s) == 3:
            chain = tuple([2] * s[2])
            l3 = lemma2_extended_path(chain)
            if args.verbose:
                print("l3", l3, pathQ(l3), cycleQ(l3))
            print(f"{len(l3)} of {multinomial(s)} permutations found. Cycle; {cycleQ(l3)}, Path; {pathQ(l3)}")

        elif len(s) == 4:
            l8 = lemma8(s)
            if args.verbose:
                print("l8", l8, pathQ(l8), cycleQ(l8))
            print(f"Lemma 8: {len(l8)} of {2*math.comb(sum(s), s[3])} permutations found. Cycle; {cycleQ(l8)}")
            x, y = _lemma8_helper([(0, 1), (1, 1), (0, s[2]-1), (1, s[3]-1)])
            if s[2] % 2 == 1 and s[3] % 2 == 1:
                perms_odd = HpathNS(s[2], s[3])
                print(f"Both {s[2]} and {s[3]} are odd: {len(set(perms_odd))}/{len(perms_odd)}/{math.comb(s[2] + s[3], s[3])}")
                print(perms_odd, pathQ(perms_odd), cycleQ(perms_odd))

        elif len(s) == 5:
            l9 = lemma9(s)
            if args.verbose:
                print("l9", l9, pathQ(l9), cycleQ(l9))
            print(f"Lemma 9: {len(l9)} of {2*math.comb(sum(s), s[4])} permutations found. Cycle; {cycleQ(l9)}")
