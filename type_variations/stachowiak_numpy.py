import argparse
import copy
import math

from helper_operations.path_operations import adjacent, cutCycle, cycleQ, pathQ
from helper_operations.permutation_graphs import multinomial
from type_variations.steinhaus_johnson_trotter_numpy import SteinhausJohnsonTrotter
from type_variations.verhoeff_numpy import HpathNS
import numpy as np


def split_path_in_2(p: np.ndarray, a: np.array) -> tuple[np.ndarray, np.ndarray]:
    assert len(p) > 1
    A = np.where((p == a).all(axis=1))[0][0]
    return p[: A + 1], p[A + 1 :]


def generate_all_di(chain_p: np.ndarray[int]) -> np.ndarray:
    """This function corresponds to the start of the proof of Lemma 2 (case 2.1 if |P| even)"""
    q = np.array([0, 1], dtype=int)
    d_all = []

    for j in range(len(chain_p) + 1):
        d_i = np.empty((0, len(chain_p) + 2), dtype=int)
        for i in range(len(chain_p) + 1 - j):
            d_i = np.vstack(
                (
                    d_i,
                    np.concatenate(
                        (chain_p[:i], [q[0]], chain_p[i + j :], [q[1]], chain_p[:j]),
                        dtype=int,
                    ),
                )
            )
        for i in reversed(range(len(chain_p) + 1 - j)):
            d_i = np.vstack(
                (
                    d_i,
                    np.concatenate(
                        (chain_p[:i], [q[1]], chain_p[i + j :], [q[0]], chain_p[:j]),
                        dtype=int,
                    ),
                )
            )
        d_all.append(d_i)
    return np.array(
        [
            np.array([np.array(item, dtype=int) for item in sublist], dtype=object)
            for sublist in d_all
        ],
        dtype=object,
    )


def generate_all_di_prime(chain_p: np.array) -> np.ndarray:
    """This function corresponds to the start of the proof of Lemma 2 (case 2.2 if |P| even)"""
    q = np.array([0, 1])
    d_all = []

    for j in range(len(chain_p) + 1):
        d_i = np.empty((0, len(chain_p) + 2), dtype=int)
        for i in range(len(chain_p) + 1 - j):
            d_i = np.vstack(
                (
                    d_i,
                    np.concatenate(
                        (chain_p[:i], [q[1]], chain_p[i + j :], [q[0]], chain_p[:j]),
                        dtype=int,
                    ),
                )
            )
        for i in reversed(range(len(chain_p) + 1 - j)):
            d_i = np.vstack(
                (
                    d_i,
                    np.concatenate(
                        (chain_p[:i], [q[0]], chain_p[i + j :], [q[1]], chain_p[:j]),
                        dtype=int,
                    ),
                )
            )
        d_all.append(d_i)
    return np.array(
        [
            np.array([np.array(item, dtype=int) for item in sublist], dtype=object)
            for sublist in d_all
        ],
        dtype=object,
    )


def lemma2_cycle(chain_p: np.array, case_2_1=True) -> np.ndarray:
    """
    This function generates the cycles of Lemma 2.
    If |P| is even the last two nodes are discarded as in the Lemma.
    Defaults to case 2.1 of Lemma 2. If the case_2_1 variable is set to false, the cycle will be as in case 2.2
    """
    if case_2_1:
        d_all = generate_all_di(chain_p)
    else:
        d_all = generate_all_di_prime(chain_p)
    # chain_1_1_path, last_elements = [], []
    chain_1_1_path = np.empty((0, len(chain_p) + 2), dtype=int)
    last_elements = np.empty((0, len(chain_p) + 2), dtype=int)
    for index, d_i in enumerate(d_all):
        # in case the |P| is even, don't add the elements 01l^p and 10l^p
        if index == len(d_all) - 1 and len(d_all) % 2 == 1:
            continue
        # never add the last elements, those will be added at the end to create a cycle
        if index % 2 == 0:
            # add the reversed list without the last element
            chain_1_1_path = np.vstack((chain_1_1_path, np.flip(d_i[:-1], axis=0)))
        else:
            chain_1_1_path = np.vstack((chain_1_1_path, d_i[:-1]))
        # keep track of the last elements
        last_elements = np.vstack((last_elements, [d_i[-1]]))
    # add the last elements of every d_i to complete the cycle
    cycle = np.concatenate((np.flip(last_elements, axis=0), chain_1_1_path), axis=0)
    assert cycleQ(cycle)
    return cycle


def lemma2_extended_path(chain_p: np.array, case_2_1=True) -> np.ndarray:
    """
    Extends the cycle of Lemma 2 with the last two elements in case |P| is even
    if |P| odd the cycle is returned
    Defaults to case 2.1 of Lemma 2. If the case_2_1 variable is set to false, the path will be as in case 2.2
    """
    cycle = lemma2_cycle(chain_p, case_2_1)
    if len(chain_p) % 2 == 0:
        if case_2_1:
            pre_path = np.array(
                [np.concatenate(([0, 1], chain_p)), np.concatenate(([1, 0], chain_p))],
                dtype=int,
            )
        else:
            pre_path = np.array(
                [np.concatenate(([1, 0], chain_p)), np.concatenate(([0, 1], chain_p))],
                dtype=int,
            )
        path = np.concatenate((pre_path, cycle), axis=0)
        assert pathQ(path)
        return path
    return cycle


def _lemma8_helper(sig_occ: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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
    k_q = np.full(sig_occ[2][1], sig_occ[2][0])
    l_p = np.full(sig_occ[3][1], sig_occ[3][0])
    if sig_occ[3][1] == 1:
        q = np.tile(np.array([first_char, second_char]), (sig_occ[2][1] + 1, 1))
        q2 = np.tile(np.array([second_char, first_char]), (sig_occ[2][1] + 1, 1))
        cycle1 = np.empty((0, len(np.concatenate((k_q, l_p)))), dtype=int)
        cycle2 = np.empty((0, len(np.concatenate((k_q, l_p)))), dtype=int)
        for index in range(sig_occ[2][1] + 1):
            cycle1 = np.vstack(
                (cycle1, np.concatenate((k_q[index:], l_p, k_q[:index]), axis=0))
            )
            cycle2 = np.vstack(
                (cycle2, np.concatenate((k_q[:index], l_p, k_q[index:]), axis=0))
            )
        cycle1 = np.vstack((cycle1, cycle2))
        q = np.vstack((q, q2))
        return q, cycle1
    else:
        all_q = np.empty((0, 2), dtype=int)
        end_q = np.empty((0, 2), dtype=int)
        result = np.empty((0, len(k_q) + len(l_p)), dtype=int)
        end_res = np.empty((0, len(k_q) + len(l_p)), dtype=int)
        for i in reversed(range(sig_occ[2][1] + 1)):
            q, g_i = _lemma8_helper(
                np.subtract(sig_occ, np.array([[0, 0], [0, 0], [0, i], [0, 1]]))
            )
            ge = np.empty((0, i + 1 + len(g_i[0])), dtype=int)
            for j, suffix in enumerate(g_i):
                node = np.concatenate((k_q[:i], [l_p[0]], suffix))
                ge = np.vstack((ge, node))
            if i % 2 != sig_occ[2][1] % 2:
                all_q = np.concatenate((all_q, np.flip(q[1:], axis=0)), axis=0)
                result = np.concatenate((result, np.flip(ge[1:], axis=0)), axis=0)
            else:
                all_q = np.concatenate((all_q, q[1:]), axis=0)
                result = np.concatenate((result, ge[1:]), axis=0)
            end_q = np.concatenate((end_q, [q[0]]), axis=0)
            end_res = np.concatenate((end_res, [ge[0]]), axis=0)
        all_q = np.vstack((all_q, np.flip(end_q, axis=0)))
        result = np.vstack((result, np.flip(end_res, axis=0)))
        return all_q, result


def _lemma7_constructor(sig: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
    We assume sig has the form [1, 1, q, p]
    """
    return _lemma8_helper(
        np.array([[0, 1], [1, 1], [2, sig[2]], [3, sig[3]]], dtype=np.int32)
    )


def lemma7(sig: np.ndarray) -> np.ndarray:
    """
    The graph G=GE( (0|1) (k^q|l^p) ) contains a Hamilton cycle for every p, q > 0
    We assume sig has the form [1, 1, q, p]
    """
    q, suffix = _lemma7_constructor(sig)
    cycle = np.array([np.concatenate((q[i], suffix[i])) for i in range(len(q))])
    try:
        assert cycleQ(cycle)
    except AssertionError as e:
        print(f"{repr(e)} in Lemma 7 for cycle: {cycle}")
        quit()
    return cycle


def _cycle_cut_start_end(cyc: np.ndarray, x: np.array, y: np.array) -> np.ndarray:
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
        print(f"{repr(err)} in 'cycle-cut-start-end' not a cycle: {cyc}")
        quit()
    try:
        assert x in cyc and y in cyc
    except AssertionError as err:
        print(f"{repr(err)} for x: {x}, y: {y}, not in cycle: {cyc}")
        quit()
    cyc_cut = cutCycle(cyc, x)
    if np.array_equal(cyc_cut[1], y):
        res = np.flip(np.vstack((cyc_cut[1:], cyc_cut[:1])), axis=0)
        assert cycleQ(res)
        return res
    assert cycleQ(cyc_cut)
    return cyc_cut


def _lemma8_g_i_sub_graphs(k_q: np.array, l_p: np.array, sig: np.ndarray) -> np.ndarray:
    """
    Creates the G_i sub graphs of Lemma 8 (by making the G_ij sub graphs and connecting them)
    :param k_q: chain of q elements "k"
    :param l_p: chain of p element "l"
    :param sig: signature of the sequence; form 1,1,q,p
    :return: [ G_1, G_2, ... ]
    """
    g_all = []
    for i in range(1, len(l_p) + 1):
        g_i = np.empty((0, np.sum(sig)), dtype=int)
        for j in range(len(l_p) - i + 1):
            g_ij = np.empty((0, np.sum(sig)), dtype=int)
            # 0 <= j < (p-i)/2
            if j < (len(l_p) - i) / 2:
                l7_q_set, l7_suffix = _lemma8_helper(
                    np.array([(0, 1), (3, 1), (2, len(k_q)), (3, i)], dtype=np.int32)
                )
                for l7_i in range(len(l7_q_set)):
                    g_ij = np.vstack(
                        (
                            g_ij,
                            np.array(
                                [
                                    *l_p[: 2 * j],
                                    *l7_q_set[l7_i],
                                    *l_p[: len(l_p) - i - 2 * j - 1],
                                    1,
                                    *l7_suffix[l7_i],
                                ]
                            ),
                        )
                    )
                x_ij = np.array(
                    [*l_p[: 2 * j], 0, *l_p[: len(l_p) - i - 2 * j], 1, *l_p[:i], *k_q]
                )
                y_ij = np.array(
                    [
                        *l_p[: 2 * j + 1],
                        0,
                        *l_p[: len(l_p) - i - 2 * j - 1],
                        1,
                        *l_p[:i],
                        *k_q,
                    ]
                )
            # j == (p-i)/2
            elif j == (len(l_p) - i) / 2:
                l7_subgraph = lemma7(np.concatenate((sig[:3], [i])))
                for item in l7_subgraph:
                    g_ij = np.vstack((g_ij, np.array([*l_p[: len(l_p) - i], *item])))
                x_ij = np.array([*l_p[: len(l_p) - i], 0, 1, *l_p[:i], *k_q])
                y_ij = np.array([*l_p[: len(l_p) - i], 1, 0, *l_p[:i], *k_q])
            # (p-i)/2 < j <= p-i
            else:
                l7_q_set, l7_suffix = _lemma8_helper(
                    np.array([(3, 1), (1, 1), (2, sig[2]), (3, i)], dtype=np.int32)
                )
                for l7_i in range(len(l7_q_set)):
                    g_ij = np.vstack(
                        (
                            g_ij,
                            np.array(
                                [
                                    *l_p[: 2 * (len(l_p) - i - j)],
                                    *l7_q_set[l7_i],
                                    *l_p[: i + 2 * j - len(l_p) - 1],
                                    0,
                                    *l7_suffix[l7_i],
                                ]
                            ),
                        )
                    )
                x_ij = np.array(
                    [
                        *l_p[: 2 * (len(l_p) - i - j) + 1],
                        1,
                        *l_p[: i + 2 * j - len(l_p) - 1],
                        0,
                        *l_p[:i],
                        *k_q,
                    ]
                )
                y_ij = np.array(
                    [
                        *l_p[: 2 * (len(l_p) - i - j)],
                        1,
                        *l_p[: i + 2 * j - len(l_p)],
                        0,
                        *l_p[:i],
                        *k_q,
                    ]
                )
            g_ij = _cycle_cut_start_end(g_ij, x_ij, y_ij)
            g_i = np.vstack((g_i, g_ij))

        if np.array_equal(
            g_i[0], np.array([0, *l_p[: len(l_p) - i], 1, *l_p[:i], *k_q])
        ):
            g_all.append(g_i)
        else:
            g_all.append(np.flip((g_i), axis=0))
    return np.array(g_all, dtype=object)


def _lemma9_glue_a_edges(
    k_r: np.array, k_s: np.array, l_p: np.array, p: int, sub_cycles: np.ndarray
) -> np.ndarray:
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
        return sub_cycles
    if len(k_s) > 0:
        g_result_start = _cycle_cut_start_end(
            np.asarray(sub_cycles[0], dtype=int),
            np.concatenate(
                (
                    k_r,
                    np.array([0]),
                    l_p[: p - 1],
                    np.array([1]),
                    np.array([k_s[0], l_p[0]]),
                    k_s[1:],
                )
            ),
            np.concatenate(
                (k_r, np.array([0]), l_p[: p - 1], np.array([1, l_p[0]]), k_s)
            ),
        )
    else:
        g_result_start = _cycle_cut_start_end(
            np.asarray(sub_cycles[0], dtype=int),
            np.concatenate(
                (
                    np.array([0]),
                    l_p[: p - 1],
                    np.array([1]),
                    np.array([k_r[0], l_p[0]]),
                    k_r[1:],
                )
            ),
            np.concatenate((np.array([0]), l_p[: p - 1], np.array([1, l_p[0]]), k_r)),
        )
    g_result_end = np.empty((0, len(k_r) + len(k_s) + len(l_p) + 2), dtype=int)
    # for each of the floor((p+1)/2) sub cycles
    for i in range(1, len(sub_cycles) - ((p + 1) % 2)):
        # take the first a1 and a2 and make them into a cycle from a1 ~ all nodes in cycle ~ a2
        a_2i_1 = np.concatenate(
            (k_r, np.array([0]), l_p[: p - 2 * i], np.array([1]), l_p[: 2 * i], k_s),
            dtype=int,
        )
        a_2i_2 = np.concatenate(
            (
                k_r,
                np.array([0]),
                l_p[: p - 2 * i],
                np.array([1]),
                l_p[: 2 * i - 1],
                np.array([k_s[0], l_p[0]]),
                k_s[1:],
            ),
            dtype=int,
        )
        cyc = _cycle_cut_start_end(np.asarray(sub_cycles[i], dtype=int), a_2i_1, a_2i_2)
        # then cut that cycle in 2 by splitting after the next a1 (and thus before the next a2)
        next_a_2 = np.concatenate(
            (
                k_r,
                np.array([0]),
                l_p[: max(p - ((2 * i) + 1), 0)],
                np.array([1]),
                l_p[: (2 * i) + 1],
                k_s,
            ),
            dtype=int,
        )
        p1, p2 = split_path_in_2(cyc, next_a_2)
        g_result_start = np.concatenate((g_result_start, p1))
        g_result_end = np.concatenate((g_result_end, np.flip(p2, axis=0)))
    if p % 2 == 0:
        # if p is even, we are still missing the last cycle which we only have to sort from the last a1~nodes~a2
        a_last_1 = np.concatenate((k_r, np.array([0, 1]), l_p, k_s))
        a_last_2 = np.concatenate(
            (k_r, np.array([0, 1]), l_p[:-1], np.array([k_s[0], l_p[-1]]), k_s[1:])
        )
        g_result_start = np.concatenate(
            (g_result_start, _cycle_cut_start_end(sub_cycles[-1], a_last_1, a_last_2))
        )
    g_result_start = np.concatenate((g_result_start, np.flip(g_result_end, axis=0)))
    return g_result_start


def lemma8(sig: np.array) -> np.ndarray:
    """
    The graph G=GE( ((0|1) k^q) | l^p) ) contains a Hamilton cycle for every p, q > O.
    We assume sig has the form [1, 1, q, p]
    """
    k_q = np.full(sig[2], 2, dtype=int)
    l_p = np.full(sig[3], 3, dtype=int)
    g_0 = np.empty((0, np.sum(sig)), dtype=int)
    g_0_end = np.empty((0, np.sum(sig)), dtype=int)
    for i in range(sig[3] + 1):
        g_0 = np.vstack(
            (
                g_0,
                np.concatenate(
                    (l_p[:i], np.array([0]), l_p[i:], np.array([1]), k_q), axis=0
                ),
            )
        )
        g_0_end = np.vstack(
            (
                g_0_end,
                np.concatenate(
                    (l_p[i:], np.array([1]), l_p[:i], np.array([0]), k_q),
                    axis=0,
                    dtype=int,
                ),
            )
        )
    # append g0end to g0
    g_0 = np.vstack((g_0, g_0_end))
    # only append lemma 8 subgraphs if p > 0
    if sig[3] == 0:
        return g_0
    lemma8_sub_graphs = _lemma8_g_i_sub_graphs(k_q, l_p, sig)
    g_all = [g_0]
    g_all.extend(lemma8_sub_graphs)

    sub_cycles = np.array(
        [np.vstack((g_all[0], np.flip(g_all[1], axis=0)))], dtype=object
    )
    sub_cycles = np.array(
        [
            np.array([np.array(item, dtype=int) for item in sublist], dtype=object)
            for sublist in sub_cycles
        ],
        dtype=object,
    )
    for i in range(2, len(g_all) - (len(g_all) % 2), 2):
        new_cycle = np.vstack((g_all[i], np.flip(g_all[i + 1], axis=0)))
        temp = list(sub_cycles)
        temp.append(new_cycle)
        sub_cycles = np.array(temp, dtype=object)
    if len(g_all) % 2 == 1:
        temp = list(sub_cycles)
        temp.append(g_all[-1])
        sub_cycles = np.array(temp, dtype=object)
    sub_cycles = np.array(
        [np.array(list(map(np.array, sublist)), dtype=int) for sublist in sub_cycles],
        dtype=object,
    )
    g_result_start = _lemma9_glue_a_edges(
        np.array([], dtype=int), k_q, l_p, sig[3], sub_cycles
    )
    return g_result_start


def lemma9(sig: np.array) -> np.ndarray:
    """
    The graph G=GE( (k^r (0|1) k^s) | l^p) ) contains a Hamilton cycle for every p, r+s > O.
    We assume sig has the form [1, 1, r, s, p]
    """
    k_r = np.full(sig[2], 2)
    k_s = np.full(sig[3], 2)
    l_p = np.full(sig[4], 3)
    # if s == 0
    if sig[2] == 0:
        return lemma8(np.concatenate((sig[:2], sig[3:])))
    # if r == 0
    if sig[3] == 0:
        # reverse every individual item before returning it
        return np.array(
            [np.flip(x) for x in lemma8(np.concatenate((sig[:3], sig[4:])))]
        )
    else:
        # r > 0
        G = []
        for i in range(len(l_p) + 1):
            # induction on r, for every 0 \leq i \leq p
            g = lemma9(np.array([sig[0], sig[1], sig[2] - 1, sig[3], i]))
            # Initialize recursive_lists with the first item from g
            recursive_lists = np.concatenate(
                (l_p[: len(l_p) - i], k_r[:1], g[0]), axis=0
            )
            # Start the loop from the second item in g
            for item in g[1:]:
                recursive_lists = np.vstack(
                    (
                        recursive_lists,
                        np.concatenate((l_p[: len(l_p) - i], k_r[:1], item), axis=0),
                    )
                )
            # a_i = l^{p-i} k l^i k^{r-1} 01 k^s
            ai = np.concatenate(
                (
                    l_p[: len(l_p) - i],
                    k_r[:1],
                    l_p[:i],
                    k_r[: len(k_r) - 1],
                    [0, 1],
                    k_s,
                )
            )
            ai_index = np.where((recursive_lists == ai).all(axis=1))[0][0]
            # l^{p-i} k l^i k^{r-1} 01 k^s
            aj = np.concatenate(
                (
                    l_p[: len(l_p) - i],
                    k_r[:1],
                    l_p[:i],
                    k_r[: len(k_r) - 1],
                    [1, 0],
                    k_s,
                )
            )
            aj_index = np.where((recursive_lists == aj).all(axis=1))[0][0]

            # fix the orientation of the list
            if ai_index > aj_index:
                recursive_lists = np.flip(recursive_lists, axis=0)
                ai_index = np.where((recursive_lists == ai).all(axis=1))[0][0]
            recursive_lists = np.roll(recursive_lists, -ai_index, axis=0)
            G.append(recursive_lists)
        G_np = np.array(
            [
                np.array([np.array(list, dtype=int) for list in sublist])
                for sublist in G
            ],
            dtype=object,
        )

        cycle = np.array(G_np[0])
        for i, item in enumerate(G_np[1:], start=1):
            if i == 1:
                # this will be the first three nodes of the path: (connecting G_0 and G_1)
                # [l^{p-1} k l k^{r-1} 01 k^s, l^p k^r 01 k^s, l^p k^r 10 k^s, l^{p-1} k l k^{r-1} 10 k^s]
                cycle = np.vstack(([item[0]], cycle, item[1:]))
            # now glue b1 and b2, b3 and b4 etc. and glue a2 and a3, a4 and a5 etc.
            elif i % 2 == 0:
                flipped_item = np.flip(item, axis=0)
                cycle = np.vstack((flipped_item[-1], cycle, flipped_item[:-1]))
            else:
                cycle = np.vstack(([item[0]], cycle, item[1:]))
        return cycle


def _lemma10_subcycle_cutter(
    cycle: np.ndarray, gi: np.ndarray, edge_i: np.array, edge_j: np.array
) -> tuple[np.ndarray, np.ndarray]:
    """
    Cuts the cycle and gi to change them for lemma 10
    :param cycle: cycle to cut for lemma 10
    :param gi: subgraph to cut for lemma 10
    :param edge_i: edge that should be at the start of gi
    :param edge_j: edge that should be the point at which the cycle is cut (see return)
    :return: cycle starts with edge_i[0] and edge_i[1] is the second node
             gi starts with edge_j[0] and edge_j[1] is the last node
    """
    ind_node_i = np.where((gi == edge_i[0]).all(axis=1))[0][0]
    # preparing gi so that node_i[0] the first and node_i[1] second in list
    if np.array_equal(gi[(ind_node_i + 1) % (len(gi) - 1)], edge_i[1]):
        gi = np.concatenate((gi[ind_node_i:], gi[:ind_node_i]))
    else:
        gi = np.flip(gi, axis=0)
        ind_node_i = np.where((gi == edge_i[0]).all(axis=1))[0][0]
        gi = np.roll(gi, -ind_node_i, axis=0)

    ind_node_j = np.where((cycle == edge_j[0]).all(axis=1))[0][0]
    # preparing the cycle (already glued ones) such that node_j[0] first and node_j[1] last in list
    if ind_node_j + 1 == len(cycle):
        # if cycle ends with node_j[0] and ends with node_j[1]
        if np.array_equal(cycle[0], edge_j[1]):
            cycle = np.flip(cycle, axis=0)
        # if cycle ends with node_j[0] and node_j[1] is the second to last element (since they are always neighbors in the path)
        else:
            # move node_j[0] to the start and append the rest of the cycle
            cycle = np.concatenate(([cycle[-1]], cycle[:-1]))
    elif np.array_equal(cycle[ind_node_j + 1], edge_j[1]):
        # if node_j[1] is the second element in the cycle
        # change cycle to start with node_j[1] and then append the part until node_j[0]. Then reverse the whole cycle
        cycle = np.roll(cycle, -ind_node_j - 1, axis=0)
        cycle = np.flip(cycle, axis=0)
    else:
        # otherwise we have [node_j[1], node_j[0], ...] so we move node_j[0] to the start and append the part until node_j[1]
        cycle = np.roll(cycle, -ind_node_j, axis=0)
    return cycle, gi


def _lemma10_helper(K: np.ndarray, p: int, new_color: int) -> np.ndarray:
    """
    :param K: Hamiltonian path in Q ([K_1, K_2, ..., K_2n])
    :param p: is the length of the last part of the signature (l^p)
    :param new_color: is the new color to add to the graph
    :return Hamiltonian path over Q | l^p
    """
    # G_i = GE(K_{2i-1} | l^p, K_{2i} | l^p) for 0 <= i <= n
    G = []
    l_p = np.full(p, new_color)
    for i in range(len(K) // 2):
        # Constructing cycles Ci taking graphs 'including' vertices on 2*i and 2*i+1 position
        for j, item in enumerate(K[2 * i]):
            # determining r and s - location of a swap
            if item != K[2 * i + 1][j]:
                r = j
                s = len(K[2 * i]) - r - 2
                break
        # G_i is isomorphic to GE( (k^r (0|1) k^s) | l^p )
        g = lemma9(np.array([1, 1, r, s, p]))

        g_modified = np.empty((0, len(g[0])), dtype=int)
        remove_color = 3
        for item in g:
            new_item = np.array(item)  # Convert item to a list
            # smartly renaming permutations -> isomorphism, depending on order of 01/10 -
            # tells us either to use 2*2 or 2*i+1
            if np.where(new_item == 0)[0][0] < np.where(new_item == 1)[0][0]:
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
            g_modified = np.vstack((g_modified, new_item))  # adding item to the array
        G.append(g_modified)  # adding cycle to the list of G_i's
    G_np = np.array(
        [np.array([np.array(list, dtype=int) for list in sublist]) for sublist in G],
        dtype=object,
    )

    cycle = G_np[0]
    # TODO, hier zit de fout onder
    # K_j = k_{j,1} k_{j,2} \dots k_{j,q}
    for i, gi in enumerate(copy.deepcopy(G_np[1:]), start=1):
        # a_i = (l^p k_{2i}, l^{p-1} k_{2i,1} l k{2i,2} \dots k_{2i,q})
        ai = np.array(
            [
                np.concatenate((l_p, K[2 * i])),
                np.concatenate((l_p[:-1], [K[2 * i][0]], l_p[-1:], K[2 * i][1:])),
            ]
        )
        # b_i = (k_{2i} l^p, k_{2i,1} \dots k_{2i,q-1} l k_{2i,q} l^{p-1})
        bi = np.array(
            [
                np.concatenate((K[2 * i], l_p)),
                np.concatenate((K[2 * i][:-1], l_p[-1:], [K[2 * i][-1]], l_p[:-1])),
            ]
        )
        # a_j = (l^p k_{2i-1}, l^{p-1} k_{2i-1,1} l k_{2i-1,2} \dots, k_{2i-1,q})
        aj = np.array(
            [
                np.concatenate((l_p, K[2 * i - 1])),
                np.concatenate(
                    (l_p[:-1], [K[2 * i - 1][0]], l_p[-1:], K[2 * i - 1][1:])
                ),
            ]
        )
        # b_j = (k_{2i-1} l^p, k_{2i-1,1} \dots k_{2i-1,q-1} l k_{2i-1,q} l^{p-1})
        bj = np.array(
            [
                np.concatenate((K[2 * i - 1], l_p)),
                np.concatenate(
                    (K[2 * i - 1][:-1], l_p[-1:], [K[2 * i - 1][-1]], l_p[:-1])
                ),
            ]
        )
        # if K_j and K_{j+1} differ in the first pair of elements, a_j and a_{j+1} are parallel
        if adjacent(ai[0], aj[0]) and adjacent(ai[1], aj[1]):
            cycle, gi = _lemma10_subcycle_cutter(cycle, gi, ai, aj)
        # if K_j and K_{j+1} don't differ in the first pair of elements, b_j and b_{j+1} are parallel
        elif adjacent(bi[0], bj[0]) and adjacent(bi[1], bj[1]):
            cycle, gi = _lemma10_subcycle_cutter(cycle, gi, bi, bj)
        cycle = np.concatenate(([gi[0]], cycle, gi[1:]))
    sig_list = np.full(len(K[0]) + 1, 0, dtype=int)
    for el in G[0][0]:
        sig_list[el] += 1
    sig_list = sig_list[sig_list != 0]
    return cycle


def lemma10(sig: np.ndarray) -> np.ndarray:
    """If q = |Q| > 2, Q is even and GE(Q) contains a Hamiltonian path and p > 0 then GE(Q|l^p) has a Hamiltonian cycle."""
    K = HpathNS(sig[0], sig[1])
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig: np.ndarray) -> np.ndarray:
    """If q = |Q| > 2, p = |P| > 0 and GE(Q) has an even number of vertices and contains a Hamiltonian path then GE(Q|P) has a Hamiltonian cycle."""
    if np.sum(sig[:2]) > 2:
        path = HpathNS(sig[0], sig[1])  # K in the paper
        next_color = 2
    elif sig[2] == 1:
        # use the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle if the first 3 (or more) elements are 1
        try:
            next_color = np.where(sig != 1)[0][0]
        except IndexError:
            next_color = len(sig)  # all elements are 1
        path = SteinhausJohnsonTrotter.get_sjt_permutations(
            SteinhausJohnsonTrotter(), next_color
        )
    elif sig[2] != 0:
        # use Stachowiak's lemma 2 to find a Hamiltonian path in GE(Q|P[1])
        path = lemma2_extended_path(np.full(sig[2], 2))
        next_color = 3
    else:
        raise ValueError(
            "q = |Q| > 2 and GE(Q) has an even number of vertices is required for Lemma 11"
        )
    for ind, new_color in enumerate(sig[next_color:], start=next_color):
        cycle = _lemma10_helper(path, new_color, ind)
        path = cycle
    return path


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

    args = parser.parse_args()
    s = np.array([int(x) for x in args.signature.split(",")])
    if len(s) > 1:
        if len(s) == 2:
            perms_odd = HpathNS(s[0], s[1])
            if args.verbose:
                print(f"Resulting path {perms_odd}")
            print(
                f"Verhoeff's result for k0={s[0]} and k1={s[1]}: {len(np.unique(perms_odd, axis=1))}/{len(perms_odd)}/{math.comb(s[0] + s[1], s[1])} "
                f"is a path: {pathQ(perms_odd)} and a cycle: {cycleQ(perms_odd)}"
            )
        elif s[0] % 2 == 0 or s[1] % 2 == 0:
            raise ValueError(
                "The first two elements of the signature should be odd for Stachowiak's permutations"
            )
        else:
            if len(s) == 3:
                pass
            l11 = lemma11(s)
            if args.verbose:
                print(f"lemma 11 results {l11}")
            print(
                f"lemma 11 {len(set(tuple(row) for row in l11))}/{len(l11)}/{multinomial(s)} is a path: {pathQ(l11)} and a cycle: {cycleQ(l11)}"
            )
