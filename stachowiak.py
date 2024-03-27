import argparse
import collections
import itertools
import math
from typing import Tuple, Union

from permutation_graphs import *
from path_operations import *


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
            q, g_i = _lemma8_helper(sig_occ[:2] + [(2, sig_occ[2][1]-i)] + [(3, sig_occ[3][1]-1)])
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
        assert cycleQ(cyc)
    except AssertionError as err:
        print(f"{repr(err)} for x: {x}, y: {y}, cycle: {cyc}")
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
    for i in range(1, sig[3] + 1):
        g_i = []
        for j in range(sig[3] - i + 1):
            g_ij = []
            # O <= j < (p-i)/2
            if j < (sig[3] - i) / 2:
                l7_q_set, l7_suffix = _lemma8_helper([(0, 1), (3, 1), (2, sig[2]), (3, i)])
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(l_p[:2 * j] + l7_q_set[l7_i] + l_p[:sig[3] - i - 2 * j - 1] + (1,) + l7_suffix[l7_i])
                g_ij = _lemma8_subgraph_cutter(
                    g_ij,
                    l_p[:2 * j] + (0,) + l_p[:sig[3] - i - 2 * j] + (1,) + l_p[:i] + k_q,
                    l_p[:2 * j + 1] + (0,) + l_p[:sig[3] - i - 2 * j - 1] + (1,) + l_p[:i] + k_q,
                )
            # j == (p-i)/2
            elif j == (sig[3] - i) / 2:
                l7_subgraph = lemma7(sig[:3] + [i])
                for item in l7_subgraph:
                    g_ij.append(l_p[:sig[3] - i] + item)
                g_ij = _lemma8_subgraph_cutter(
                    g_ij,
                    l_p[:sig[3] - i] + (0, 1) + l_p[:i] + k_q,
                    l_p[:sig[3] - i] + (1, 0) + l_p[:i] + k_q,
                )
            # (p-i)/2 < j <= p-i
            else:
                l7_q_set, l7_suffix = _lemma8_helper([(3, 1), (1, 1), (2, sig[2]), (3, i)])
                for l7_i in range(len(l7_q_set)):
                    g_ij.append(
                        l_p[:2 * (sig[3] - i - j)] + l7_q_set[l7_i] + l_p[:i + 2 * j - sig[3] - 1] + (0,) + l7_suffix[
                            l7_i])
                g_ij = _lemma8_subgraph_cutter(
                    g_ij,
                    l_p[:2 * (sig[3] - i - j) + 1] + (1,) + l_p[:i + 2 * j - sig[3] - 1] + (0,) + l_p[:i] + k_q,
                    l_p[:2 * (sig[3] - i - j)] + (1,) + l_p[:i + 2 * j - sig[3]] + (0,) + l_p[:i] + k_q,
                )
            g_i.extend(g_ij)
        if g_i[0] == ((0,) + l_p[:sig[3] - i] + (1,) + l_p[:i] + k_q):
            g_all.append(g_i)
        else:
            g_all.append(g_i[::-1])
    return g_all


def _lemma8_glue_a_edges(k_q: Tuple[int, ...], l_p: Tuple[int, ...], p: int, sub_cycles):
    """
    Glues the a_i edges from Lemma8 together to create the final cycle
    :param k_q: chain of q elements "k"
    :param l_p: chain of p element "l"
    :param p: number of l elements (sig[3])
    :param sub_cycles: sub cycles created by gluing y_ij, y_ij+1
    :return: Cycle of all sub cycles glued together
    """
    g_result_start = _lemma8_subgraph_cutter(
        sub_cycles[0],
        (0,) + l_p[:p - 1] + (1,) + (k_q[0], l_p[0]) + k_q[1:],
        (0,) + l_p[:p - 1] + (1, l_p[0]) + k_q,
    )
    g_result_end = []
    for i in range(1, len(sub_cycles)-(len(sub_cycles) % 2)):
        cyc = _lemma8_subgraph_cutter(
            sub_cycles[i],
            (0,) + l_p[:p - 2 * i] + (1,) + l_p[:2 * i] + k_q,
            (0,) + l_p[:p - 2 * i] + (1,) + l_p[:2 * i - 1] + (k_q[0], l_p[0]) + k_q[1:],
        )
        p1, p2 = splitPathIn2(cyc, (0,) + l_p[:max(p - ((2 * i) + 1), 0)] + (1,) + l_p[:(2 * i) + 1] + k_q, )
        g_result_start.extend(p1)
        g_result_end.extend(p2)
    if p % 2 == 0:
        g_result_start.extend(
            _lemma8_subgraph_cutter(sub_cycles[-1], (0, 1) + l_p + k_q, (0, 1) + l_p[:-1] + (k_q[0], l_p[-1]) + k_q[1:])
        )
    g_result_start.extend(g_result_end)
    return g_result_start


def lemma8(sig: List[int]) -> List[tuple]:
    """
     The graph G=GE( ((0|1) k^q) | l^p) ) contains a Hamilton cycle for every p, q >O.
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
    g_result_start = _lemma8_glue_a_edges(k_q, l_p, sig[3], sub_cycles)
    # assert cycleQ(g_result_start)
    return g_result_start


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper tool to find paths through permutation neighbor swap graphs.")
    parser.add_argument("-s", "--signature"
                        , type=str, help="Input permutation signature (comma separated)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args()
    sig = [int(x) for x in args.signature.split(",")]
    if len(sig) > 1:
        if sig[0] % 2 == 0 or sig[1] % 2 == 0:
            raise ValueError("The first two elements of the signature should be odd for Stachowiak's permutations")
        if len(sig) == 3:
            chain = tuple([2] * sig[2])
            print(lemma2_extended_path(chain))
            print(f"{len(lemma2_extended_path(chain))} of {multinomial([1, 1, sig[2]])} permutations found.")
        l7 = lemma7(sig)
        print("l7", l7, pathQ(l7), cycleQ(l7))
        print(f"{len(l7)}/{len(set(l7))} of {multinomial(sig)} permutations found. {2*multinomial(sig[2:])}")

        l8 = lemma8(sig)
        print("l8", l8, pathQ(l8), cycleQ(l8))
        print(f"{len(l8)}/{len(set(l8))} of {2*math.comb(sum(sig), sig[3])} permutations found.")
