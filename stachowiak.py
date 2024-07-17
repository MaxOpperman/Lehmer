import argparse
import itertools
import math

from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    cycleQ,
    get_transformer,
    pathQ,
    splitPathIn2,
    transform,
)
from helper_operations.permutation_graphs import defect, multinomial
from steinhaus_johnson_trotter import SteinhausJohnsonTrotter
from verhoeff import HpathNS


def main():
    """
    This script uses Stachowiak's theorems to find Hamiltonian cycles in neighbor-swap graphs.

    Args:
        -s, --signature: Input permutation signature (comma separated, without spaces)
        -v, --verbose: Enable verbose mode, `False` by default
        -p, --parities: Show the even and odd counts of all permutations
    Returns:
        Prints whether the result is a Hamiltonian path or cycle in the neighbor-swap graph.
        If verbose mode is enabled, it also prints the resulting path.
    Raises:
        ValueError: If the signature is empty.
        ValueError: If the signature contains negative values.
    References:
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
    """
    parser = argparse.ArgumentParser(
        description="Uses Stachowiak's theorems to find Hamiltonian cycles in neighbor-swap graphs"
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
        defect_g = defect(s)
        print(f"Defect {defect_g} for n={sum(s)}")
        if defect_g > 0:
            print(
                f"NO HAMILTONIAN CYCLE POSSIBLE: n={sum(s)} EVEN and defect={defect_g} != 0"
            )
        elif defect_g > 1:
            print(
                f"NO HAMILTONIAN CYCLE POSSIBLE: n={sum(s)} ODD and defect={defect_g} != 1"
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
        else:
            l11 = lemma11(s)
            if args.verbose:
                print(f"lemma 11 results {l11}")
            print(
                f"lemma 11 {len(set(l11))}/{len(l11)}/{multinomial(s)} is a path: {pathQ(l11)} and a cycle: {cycleQ(l11)}"
            )


def _generate_all_di(chain_p: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generate all possible `d_i` chains based on the given `chain_p`.
    This function corresponds to the start of the proof of Lemma 2 (case 2.1 if the length of `chain_p` even).

    Args:
        chain_p (tuple[int, ...]): The chain of `p` elements in the lemma.

    Returns:
        list[tuple[int, ...]]:
            All possible `d_i` chains. Each `d_i` chain is represented as a list of tuples of integers:
            `d_i=[0l^{p-i} 1 l^i, l0l^{p-i-1} 1 l^i, \cdots, l^{p-i} 01 l^i, l^{p-i} 10 l^i, \cdots, 1 l^{p-i} 0 l^i]`.
            This is for every `0 <= i <= p`.
    """
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


def _generate_all_di_prime(chain_p: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generate all possible `d_i` chains based on the given `chain_p`.
    This function corresponds to the start of the proof of Lemma 2 (case 2.2 if the length of `chain_p` even).

    Args:
        chain_p (tuple[int, ...]): The chain of p elements in Lemma 2.

    Returns:
        list[tuple[int, ...]]:
            All possible `d_i'` chains. Each `d_i'` chain is represented as a list of tuples of integers:
            `d_i'=[l^i 1 l^{p-i} 0, l^i 1 l^{p-i-1} 0 l, \cdots, l^{i} 10 l^{p-i}, l^i 01 l^{p-i}, \cdots, l^i 0 l^{p-i} 1]`.
            This is for every `0 <= i <= p`.
    """
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


def lemma2_cycle(chain_p: tuple[int, ...], case_2_1=True) -> list[tuple[int, ...]]:
    """
    This function generates the cycles of Lemma 2.
    If the length of the `chain_p` is even the last two nodes are discarded as in the lemma.
    Defaults to case 2.1 of Lemma 2. If the `case_2_1` variable is set to `False`, the cycle will be as in case 2.2. The discarded nodes are:\n
    - `d_p = (01 l^p, 10 l^p)` for case 2.1
    - `d_p' = (l^p 01, l^p 10)` for case 2.2

    Args:
        chain_p (tuple[int, ...]): The chain of p elements in the lemma
        case_2_1 (bool, optional):
            Whether the case is 2.1 or 2.2. Defaults to `True`.\n
            - `True` ==> Case 2.1 with all `d_i` paths.
            - `False` ==> Case 2.2 with all `d_i'` paths.

    Returns:
        list[tuple[int, ...]]:
            The cycle of all `d_i` or `d_i'` paths.
            If the length of `chain_p` is even, `d_p` or `d_p'` is discarded respectively to the input for `case_2_1`.
    """
    if case_2_1:
        d_all = _generate_all_di(chain_p)
    else:
        d_all = _generate_all_di_prime(chain_p)
    chain_1_1_path, last_elements = [], []
    for index, d_i in enumerate(d_all):
        # in case the |P| is even, don't add the elements 01l^p and 10l^p or l^p01 and l^p10 respectively to case 2.1 or 2.2
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
    return cycle


def lemma2_extended_path(
    chain_p: tuple[int, ...], case_2_1=True
) -> list[tuple[int, ...]]:
    """
    Extends the cycle of Lemma 2 with the last two elements in case `chain_p` is even.
    If the length of `chain_p` is odd, then the cycle is returned.
    Defaults to case 2.1 of Lemma 2. If the `case_2_1` variable is set to `False`, the path will be as in case 2.2.\r\n
    If `chain_p` is even, the two nodes which are appended to the path are;\n
    - `d_p = (01 l^p, 10 l^p)` for case 2.1
    - `d_p' = (l^p 01, l^p 10)` for case 2.2

    Args:
        chain_p (tuple[int, ...]): The chain of p elements in the lemma.
        case_2_1 (bool, optional):
            Whether the case is 2.1 or 2.2. Defaults to `True`.\n
            - `True` ==> Case 2.1 with all `d_i` paths.
            - `False` ==> Case 2.2 with all `d_i'` paths.

    Returns:
        list[tuple[int, ...]]:
            The cycle of all `d_i` or `d_i'` paths extended with the two nodes that are left out if the length of `chain_p` is even.\n
            - `d_i=[0l^{p-i} 1 l^i, l0l^{p-i-1} 1 l^i, \cdots, l^{p-i} 01 l^i, l^{p-i} 10 l^i, \cdots, 1 l^{p-i} 0 l^i]`
            - `d_i'=[l^i 1 l^{p-i} 0, l^i 1 l^{p-i-1} 0 l, \cdots, l^{i} 10 l^{p-i}, l^i 01 l^{p-i}, \cdots, l^i 0 l^{p-i} 1]`
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
    Helper function for Lemma 8 of Stachowiak:
    The graph `G=GE( (char_0|char_1) (k^q|l^p) )` contains a Hamilton cycle for every `p, q > 0`.
    `k^q` is a chain of q elements "k", `l^p` is a chain of p elements "l".
    We say the first element is `char_0` and the second element is `char_1`.

    Args:
        sig_occ (list[tuple[int, int]]):
            The signature of the neighbor-swap graph; `[1, 1, q, p]`.
            It has the form `[(int, 1), (int, 1), (int, q), (int, p)]`.
            The first two integers are of different colors and occur once.
            The last two integers are of different colors and can occur any number of times >= 0.

    Returns:
        tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
            A Hamiltonian cycle of the form `(char_0|char_1) (k^q|l^p)`.
            So the first two elements are always before the last two elements but their internal order can differ.

    Raises:
        AssertionError: If the first two elements do not occur once.
        AssertionError: If the first two elements are not of different colors.
        AssertionError: If the last two elements are not of different colors.
        AssertionError: If the last two elements occur less than 0 times.
    """
    first_char = sig_occ[0][0]
    second_char = sig_occ[1][0]
    assert sig_occ[0][1] == 1
    assert sig_occ[1][1] == 1
    assert first_char != second_char
    assert sig_occ[2][0] != sig_occ[3][0]
    assert sig_occ[2][1] >= 0 and sig_occ[3][1] >= 0
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
    sig: tuple[int],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Writes colors of Lemma 7 to fit the helper of Lemma 8 (which solves a more general version of this graph).
    Lemma 7 by Stachowiak is: The graph `G=GE( (0|1) (k^q|l^p) )` contains a Hamilton cycle for every `p, q > 0`

    Parameters:
        sig (tuple[int]):
            The signature of the graph in the form `[1, 1, q, p]`.
            The elements are of colors 0, 1, 2, 3 (so color 2 occurs `q` times and 3 occurs `p` times).
            Colors 0 and 1 occur once, colors 2 and 3 occur q and p times respectively.
            The first two elements are of different colors and the last two elements are of different colors than each other.

    Returns:
        tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
            A tuple of the q set and the suffix.\n
            - The q set is the 01 or 10 part, i.e. the first two nodes of the permutations.
            - The suffix set is the k^q and the l^p part permuted, i.e. the rest of the permutation
    """
    return _lemma8_helper([(0, 1), (1, 1), (2, sig[2]), (3, sig[3])])


def lemma7(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    Computes Lemma 7 by Stachowiak: The graph `G=GE( (0|1) (k^q|l^p) )` contains a Hamilton cycle for every `p, q > 0`.

    Args:
        sig (tuple[int]):
            The signature of the graph in the form `[1, 1, q, p]`.
            The elements are of colors 0, 1, 2, 3 (so color 2 occurs `q` times and 3 occurs `p` times).

    Returns:
        list[tuple[int, ...]]: A Hamiltonian cycle of the form `(0|1) (k^q|l^p)`
    """
    q, suffix = _lemma7_constructor(sig)
    cycle = [q[i] + suffix[i] for i in range(len(q))]
    return cycle


def _cut_cycle_start_end(
    cyc: list[tuple[int, ...]], x: tuple[int, ...], y: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    Makes sure `x` is the start node of a given cycle `cyc` and `y` is the end node.

    Args:
        cyc (list[tuple[int, ...]]): Cycle in a subgraph.
        x (tuple[int, ...]): Node that should be at the start of the path.
        y (tuple[int, ...]): Node that should be at the end of the path.

    Returns:
        list[tuple[int, ...]]: Subgraph with `x` as start and `y` as end.

    Raises:
        AssertionError: If `x` and `y` are not adjacent.
        AssertionError: If `cyc` is not a cycle.
        AssertionError: If `x` or `y` is not in the cycle.
    """
    try:
        assert adjacent(x, y)
    except AssertionError as err:
        print(f"{repr(err)} not adjacent for x: {x}, y: {y}")
        raise err
    try:
        assert cycleQ(cyc)
    except AssertionError as err:
        print(f"{repr(err)} not a cycle: {cyc}")
        raise err
    try:
        assert x in cyc and y in cyc
    except AssertionError as err:
        print(f"{repr(err)} for x: {x}, y: {y}, not in cycle: {cyc}")
        raise err
    cyc_cut = cutCycle(cyc, x)
    if cyc_cut[1] == y:
        res = (cyc_cut[1:] + cyc_cut[:1])[::-1]
        assert cycleQ(res)
        return res
    return cyc_cut


def _lemma8_g_i_sub_graphs(
    k_q: tuple[int, ...], l_p: tuple[int, ...]
) -> list[list[tuple[int, ...]]]:
    """
    Creates the G_i sub graphs of Lemma 8 by making the G_ij sub graphs and connecting them as in the lemma.
    G_{ij} is one of three cases:\n
    - G_{ij} = GE( l^(2j) (0 | l) l^(p-i-2j-1) 1(l^i | k^q) )           for 0 <= j < (p-i)/2\n
    - G_{ij} = GE( l^(p-i) (0 | 1) (l^i | k^q) )                        for j = (p-i)/2\n
    - G_{ij} = GE( l^(2(p-i-j)) (l | 1) l^(i+2j-p-1) 0(l^i | k^q) )     for (p-i)/2 < j <= p-i\r\n
    These subgraphs are connected by nodes y_{ij}, x_{i(j+1)} for different x_ij:\n
    - x_{ij} = l^(2j) 0 l^(p-i-2j) 1 l^i k^q for 0 <= j < (p-i)/2\n
    - x_{ij} = l^(p-i) 0 1 l^i k^q for j = (p-i)/2\n
    - x_{ij} = l^(2(p-i-j)+1) 1 l^(i+2j-p-1) l^i k^q for (p-i)/2 < j <= p-i\r\n
    And y_{ij}:\n
    - y_{ij} = l^(2j+1) 0 l^(p-i-2j-1) 1 l^i k^q for 0 <= j < (p-i)/2\n
    - y_{ij} = l^(p-i) 1 0 l^i k^q for j = (p-i)/2\n
    - y_{ij} = l^(2(p-i-j)) 1 l^(i+2j-p) l^i k^q for (p-i)/2 < j <= p-i\n

    Args:
        k_q (tuple[int, ...]): Chain of q elements "k"
        l_p (tuple[int, ...]): Chain of p element "l"

    Returns:
        list[list[tuple[int, ...]]]:
            List of `G_i` sub graphs: `G_i = G( (0 | l^(p-i) 1(k^q | l^i)), (1 | l^(p-i) 0(k^q | l^i)) )`
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
                l7_subgraph = lemma7([1, 1, len(k_q), i])
                for item in l7_subgraph:
                    g_ij.append(l_p[: len(l_p) - i] + item)
                x_ij = l_p[: len(l_p) - i] + (0, 1) + l_p[:i] + k_q
                y_ij = l_p[: len(l_p) - i] + (1, 0) + l_p[:i] + k_q
            # (p-i)/2 < j <= p-i
            else:
                l7_q_set, l7_suffix = _lemma8_helper(
                    [(3, 1), (1, 1), (2, len(k_q)), (3, i)]
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
            g_ij = _cut_cycle_start_end(g_ij, x_ij, y_ij)
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
    sub_cycles: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """
    Glues the a_i edges from Lemma 8 by Stachowiak together to create the final cycle.
    `a_i = ( 0 l^(p-i) 1 l^i k^q, 0 l^(p-i) 1 l^(i-1) k l k^q )`

    Args:
        k_r (tuple[int, ...]): Chain of r elements "k"
        k_s (tuple[int, ...]): Chain of s elements "k" (so  the same element as k_r but maybe a different length)
        l_p (tuple[int, ...]): Chain of p elements "l" (different from k_r and k_s)
        sub_cycles (list[tuple[int, ...]]): Sub cycles created by gluing y_{ij}, x_{i(j+1)} from Lemma 8

    Returns:
        list[tuple[int, ...]]:
            Cycle of all sub cycles glued together. Has the form `GE( (k^r (0|1) k^s) | l^p) )`
    """
    # make the a1 path, we have as first part of the cycle a11~path~a12
    if len(l_p) == 0:
        return [item for row in sub_cycles for item in row]
    p = len(l_p)
    if len(k_s) > 0:
        g_result_start = _cut_cycle_start_end(
            sub_cycles[0],
            k_r + (0,) + l_p[: p - 1] + (1,) + (k_s[0], l_p[0]) + k_s[1:],
            k_r + (0,) + l_p[: p - 1] + (1, l_p[0]) + k_s,
        )
    else:
        g_result_start = _cut_cycle_start_end(
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
        cyc = _cut_cycle_start_end(sub_cycles[i], a_2i_1, a_2i_2)
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
        g_result_start.extend(_cut_cycle_start_end(sub_cycles[-1], a_last_1, a_last_2))
    g_result_start.extend(g_result_end[::-1])
    return g_result_start


def lemma8(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    The graph `G=GE( ((0|1) k^q) | l^p) )` contains a Hamilton cycle for every `p, q > 0`

    Args:
        sig (tuple[int]):
            The signature of the neighbor-swap graph; 1, 1, q, p.
            We assume the first two elements are of colors 0 and 1 and occur once.
            The second two elements are of colors 2 and 3 and occur q and p times respectively.

    Returns:
        list[tuple[int, ...]]: A Hamiltonian cycle of the form `GE((0|1) k^q) | l^p)`
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
    g_all = [g_0] + _lemma8_g_i_sub_graphs(k_q, l_p)
    sub_cycles = []
    for i in range(0, len(g_all) - (len(g_all) % 2), 2):
        sub_cycles.append(g_all[i] + g_all[i + 1][::-1])
    if len(g_all) % 2 == 1:
        sub_cycles.append(g_all[-1])
    g_result_start = _lemma9_glue_a_edges((), k_q, l_p, sub_cycles)
    return g_result_start


def lemma9(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    The graph `G=GE( (k^r (0|1) k^s) | l^p) )` contains a Hamilton cycle for every `p, r+s > 0`.

    Args:
        sig (tuple[int]):
            The signature of the neighbor-swap graph; [1, 1, r, s, p]. We assume:\n
            - The first two elements are of colors 0 and 1 respectively and occur once.
            - The second two elements are of color 2 and occur r and s times respectively.
            - The fourth element is of color 3 and occurs p times.

    Returns:
        list[tuple[int, ...]]:
            A Hamiltonian cycle of the form `GE( (k^r (0|1) k^s) | l^p) )`
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
    edge_i: tuple[tuple[int, ...], tuple[int, ...]],
    edge_j: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Cuts the old cycle and gi (to add) to change them for Lemma 10 by Stachowiak.
    We want to glue the `cycle` and `gi` together at the `edge_i` and `edge_j` nodes.

    Args:
        cycle (list[tuple[int, ...]]): The old cycle to cut for lemma 10.
        gi (list[tuple[int, ...]]): The subgraph to cut for lemma 10, will be added later.
        edge_i (tuple[tuple[int, ...], tuple[int, ...]]):
            The edge that should be at the start of gi, i.e. position 0 and 1 in `gi`.
        edge_j (tuple[tuple[int, ...], tuple[int, ...]]):
            The edge that should be the point at which the cycle is cut, i.e. position 0 and -1 in `cycle`.

    Returns:
         tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
            The modified cycle and gi.\n
            - The gi starts with `edge_i[0]` and `edge_i[1]` is the second node.
            - The cycle starts with `edge_j[0]` and `edge_j[1]` is the last node.
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


def _lemma10_helper(
    K: list[tuple[int, ...]], p: int, new_color: int
) -> list[tuple[int, ...]]:
    """
    Helper function for lemma 10, constructs a cycle by adding color `new_color`, which occurs `p` times, to the graph

    Args:
        K (list[tuple[int, ...]]):
            A Hamiltonian path in `Q` being `[K_1, K_2, ..., K_2n]`.
            Every K_i is isomorphic to some `G_i = G(K_{2i-1} | l^p, K_{2i} | l^p)` for `1 <= i <= n`.
            And every `G_i` is isomorphic to `G_i = G((k^r (0 | 1) k^s) | l^p)`, i.e. the graph from lemma 9.
        p (int): The length of the last part of the signature (`l^p`)
        new_color (int): The new color to add to the graph (to transform `l^p`)

    Returns:
        list[tuple[int, ...]]: Hamiltonian cycle over `GE(Q | l^p)`
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
        ai = (
            l_p + K[2 * i],
            l_p[:-1] + tuple([K[2 * i][0]]) + l_p[-1:] + K[2 * i][1:],
        )
        # b_i = (k_{2i} l^p, k_{2i,1} \dots k_{2i,q-1} l k_{2i,q} l^{p-1})
        bi = (
            K[2 * i] + l_p,
            K[2 * i][:-1] + l_p[-1:] + tuple([K[2 * i][-1]]) + l_p[:-1],
        )
        # a_j = (l^p k_{2i-1}, l^{p-1} k_{2i-1,1} l k_{2i-1,2} \dots, k_{2i-1,q})
        aj = (
            l_p + K[2 * i - 1],
            l_p[:-1] + tuple([K[2 * i - 1][0]]) + l_p[-1:] + K[2 * i - 1][1:],
        )
        # b_j = (k_{2i-1} l^p, k_{2i-1,1} \dots k_{2i-1,q-1} l k_{2i-1,q} l^{p-1})
        bj = (
            K[2 * i - 1] + l_p,
            K[2 * i - 1][:-1] + l_p[-1:] + tuple([K[2 * i - 1][-1]]) + l_p[:-1],
        )
        # if K_j and K_{j+1} differ in the first pair of elements, a_j and a_{j+1} are parallel
        if adjacent(ai[0], aj[0]) and adjacent(ai[1], aj[1]):
            cycle, gi = _lemma10_subcycle_cutter(cycle, gi, ai, aj)
        # if K_j and K_{j+1} don't differ in the first pair of elements, b_j and b_{j+1} are parallel
        elif adjacent(bi[0], bj[0]) and adjacent(bi[1], bj[1]):
            cycle, gi = _lemma10_subcycle_cutter(cycle, gi, bi, bj)
        cycle = [gi[0]] + cycle + gi[1:]
    return cycle


def lemma10(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    Computes Lemma 10 by Stachowiak:
    If `q = |Q| > 2`, `Q` is even and `GE(Q)` contains a Hamiltonian path and `p > 0` then `GE(Q|l^p)` has a Hamiltonian cycle.
    Here `Q` is two elements in the signature that form a Hamiltonian path of even length and p is the third element.

    Args:
        sig (tuple[int]):
            The signature of the graph; `Q` is the first two elements, `p` is the third.
            `Q` is of length 2, its colors are 0 and 1. It contains a Hamiltonian path.
            `p` is the third element of sig and has color 2 and occurs `p` times.

    Returns:
        list[tuple[int, ...]]:
            A Hamiltonian cycle in the neighbor-swap graph of the form `GE(Q|l^p)`

    Raises:
        AssertionError:
            If the signature is not well-formed. The first two elements must be able to form a Hamiltonian path of even length > 2.
    """
    assert sig[0] + sig[1] > 2 and sig[0] % 2 == 1 and sig[1] % 2 == 1
    K = HpathNS(sig[0], sig[1])
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    Finds a Hamiltonian cycle in a graph using Lemma 11 from Stachowiak's paper:
    If `q = |Q| > 2`, `p = |P| > 0` and `GE(Q)` has an even number of vertices and contains a Hamiltonian path then `GE(Q|P)` has a Hamiltonian cycle.

    Args:
        sig (tuple[int]):
            A signature of a neighbor-swap graph where at least two elements form a Hamiltonian path of even length > 2.
            These two elements are set to the front of the signature using a recursive call.
            Note that this can also be three elements if the first two are 1 (using Lemma 2). Or at least 3 elements that occur once (using Steinhaus-Johnson-Trotter algorithm).
            The rest of the signature is processed using Stachowiak's lemmas.

    Returns:
        list[tuple[int, ...]]:
            A Hamiltonian cycle in the neighbor-swap graph of the form `GE(Q|P)`. `Q` is this Hamiltonian path and `P` is the rest of the signature

    Raises:
        ValueError: If the signature is empty.
        ValueError: There are no elements that can form a Hamiltonian path.

    Notes:
        - If `q = |Q| > 2`, `p = |P| > 0` and `GE(Q)` has an even number of vertices and contains a Hamiltonian path, then `GE(Q|P)` has a Hamiltonian cycle.
        - The function first checks the length of the signature and handles special cases where the signature has only one or two elements.
        - If the signature is not ordered well, it transforms the signature and recursively calls the function with the transformed signature. The order is well when the first two elements are the largest odd numbers.
        - If the first two elements in the signature can form a cycle (more than two permutations), it uses Verhoeff's Theorem to find the cycle.
        - If the first 3 (or more) elements are 1, it uses the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle.
        - If the third element in the signature is not 0, it uses Stachowiak's Lemma 2 to find a Hamiltonian path in `GE(Q|l^{sig[2]})`.
        - Finally, it iterates over the remaining elements in the signature and calls the helper function _lemma10_helper to extend the cycle.

    References:
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017. (Used to find Hamiltonian cycles in binary neighbor-swap graphs.)
    """
    if len(list(sig)) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(list(sig)) == 1:
        return [(0,) * sig[0]]
    elif len(list(sig)) == 2 and sig[0] == sig[1] == 1:
        return [(0, 1), (1, 0)]
    elif sum(1 for n in sig if n % 2 == 1) < 2:
        raise ValueError("At least two odd numbers are required for Lemma 11")
    sorted_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])

    # if the order is well (i.e. the first two elements are the largest odd numbers)
    # and the number of odd numbers is at least 2
    if sig != sorted_sig:
        # return that solution given by this lemma (transformed, if needed)
        return transform(lemma11(sorted_sig), transformer)
    # if the first two elements in the signature can form a cycle (so more than two permutations)
    elif sum(sig[:2]) > 2:
        # Verhoeff's Theorem to find this cycle (or path if one of the elements is 1)
        path = HpathNS(sig[0], sig[1])  # K in the paper
        next_color = 2
    # if the sum of the first two odd numbers is less than 2, then there must be more 1's in the signature
    elif sum(1 for n in sig if n % 2 == 1) > 2:
        # use the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle if the first 3 (or more) elements are 1
        try:
            next_color = sig.index(next(x for x in sig if x != 1))
        except StopIteration:
            next_color = len(list(sig))  # all elements are 1
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


if __name__ == "__main__":
    main()
