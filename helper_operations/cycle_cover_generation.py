from helper_operations.path_operations import (
    createZigZagPath,
    cutCycle,
    cycleQ,
    glue,
    pathQ,
    splitPathIn2,
)
from helper_operations.permutation_graphs import (
    extend,
    incorporateSpursInZigZag,
    stutterPermutations,
    swapPair,
)
from helper_operations.simple_verhoeff_paths import (
    Hcycle_odd_2_1,
    Hpath_even_1_1,
    Hpath_odd_2_1,
)
from verhoeff import HpathNS


def parallel_sub_cycle_odd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates the parallel cycle from the 02 and 20 cycles with stutters. Uses the createZigZagPath and incorporateSpursInZigZag functions.

    Args:
        k (int): The input value for `k`, the number of 0's\n
        This must be even because we don't count the zero in the trailing `02 / 20`

    Returns:
        list[tuple[int, ...]]: The generated path from `0 1 0^{k-1} 1 0 2` to `1 0^(k) 1 0 2`

    Raises:
        ValueError: If k is odd
    """
    if k % 2 == 1:
        raise ValueError(f"k must be even, you probably mean {k-1} and not {k}")
    cycle_without_stutters = HpathNS(k, 2)
    cycle_20_02 = cutCycle(
        createZigZagPath(cycle_without_stutters, (2, 0), (0, 2)),
        (0, 1) + (0,) * (k - 1) + (1, 0, 2),
    )
    sp02 = stutterPermutations([k, 2])
    cycle_with_stutters = incorporateSpursInZigZag(cycle_20_02, sp02, [(0, 2), (2, 0)])
    return cycle_with_stutters


def incorporated_odd_2_1_path_a_b(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from `a = 1 2 0^{k0} 1` to `b = 0 2 1 0^{k0-1} 1`.
    Including the _02 and _20 cycles (with stutters), and the _1 & _12 path.
    First generates the a_b_path, then the parallel cycles, and then splits the a_b_path in 2 at the parallel edge.
    The cross edges are:\n
    - From `0 1 0^{k-1} 1 0 2` to `0 1 0^{k0-1} 1 2`\n
    - From `1 0^k 1 0 2` to `1 0^(k) 1 0 2`.

    Args:
        k (int): The input value the number of 0s. Must be odd!

    Returns:
        list[tuple[int, ...]]:
            The generated path from `a` to `b`\n
            - `a = 1 2 0^{k0} 1`
            - `b = 0 2 1 0^{k0-1} 1`
    """
    if k % 2 == 0 or k < 0:
        raise ValueError(f"k must be odd and positive, got {k}")
    if k == 1:
        return Hpath_odd_2_1(1)

    # the path from a to b (_1 | _12) with parallel 02-20 cycles incorporated
    parallelCycles = parallel_sub_cycle_odd_2_1(k - 1)
    a_b_path = Hpath_odd_2_1(k)
    # split the a_b_path in 2 at the parallel edge with parallelCycles
    cut_node = (0, 1) + (0,) * (k - 1) + (1, 2)
    split1, split2 = splitPathIn2(a_b_path, cut_node)
    p1_p12_p02_p20 = split1 + parallelCycles + split2

    # path from c'10=120^{k_0-1}10 to d'10=0210^{k_0-1}10 (_10)
    p10 = extend(Hpath_even_1_1(k - 1), (1, 0))
    # path from a'00=120^{k_0-2}100 to b'00=0210^{k_0-3}100 (_00)
    p00 = extend(incorporated_odd_2_1_path_a_b(k - 2), (0, 0))
    cycle = p10 + p00[::-1]
    assert cycleQ(cycle)
    # make sure the cycle ends with 2 1 0^{k0} 1 0
    if not cycle[-1] == (2, 1) + (0,) * (k - 1) + (1, 0):
        cycle = cycle[:1] + cycle[1:][::-1]
    assert cycle[-1] == (2, 1) + (0,) * (k - 1) + (1, 0)
    # b = 0 2 1 0^(k-2) 1 to a = 1 2 0^(k-1) 1
    return p1_p12_p02_p20[:1] + cycle + p1_p12_p02_p20[1:]


def incorporated_odd_2_1_cycle(
    k: int, flip_stutter_cross_edge: bool = False
) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from `e = 1 0 2 0^{k0-1} 1` to `f = 0 1 2 0^{k0-1} 1`.
    Including the _02 and _20 cycles (with stutters), and the _1 & _12 path.
    First generates the a_b_path, then the parallel cycles, and then splits the a_b_path in 2 at the parallel edge.
    The cross edges are:\n
    - From `0 1 0^{k-1} 1 0 2` to `0 1 0^{k0-1} 1 2`\n
    - From `1 0^k 1 0 2` to `1 0^(k) 1 0 2`.

    Args:
        k (int): The input value the number of 0s. Must be odd!
        flip_stutter_cross_edge (bool, optional): If the cross edge should be flipped. Defaults to False; `0^{k-1} 1 0 2` to `0^{k0-1} 1 2`.

    Returns:
        list[tuple[int, ...]]:
            The generated path from `a` to `b`\n
            - `e = 1 0 2 0^{k0-1} 1`
            - `f = 0 1 2 0^{k0-1} 1`
    """
    if k % 2 == 0 or k < 0:
        raise ValueError(f"k must be odd and positive, got {k}")
    if k == 1:
        return Hpath_odd_2_1(1)

    # the path from a to b (_1 | _12) with parallel 02-20 cycles incorporated
    parallelCycles = parallel_sub_cycle_odd_2_1(k - 1)
    e_f_cylce = Hcycle_odd_2_1(k)

    # path from c'10=120^{k_0-1}10 to d'10=0210^{k_0-1}10 (_10)
    p10 = extend(Hpath_even_1_1(k - 1), (1, 0))
    # path from a'00=120^{k_0-2}100 to b'00=0210^{k_0-3}100 (_00)
    p00 = extend(incorporated_odd_2_1_path_a_b(k - 2), (0, 0))

    # generate the cycle from c=1 2 0^{k0-1} 1 0 to 2 1 0^{k0-1} 1 0
    cycle = p10 + p00[::-1]
    assert cycleQ(cycle)
    # split the cycle in two at the node 1 2 0^{k0} 1 - 2 1 0^{k0} 1
    c1_c12_c00_c10 = glue(
        e_f_cylce,
        cycle,
        (
            (0, 1, 2) + (0,) * (k - 1) + (1,),
            swapPair((0, 1, 2) + (0,) * (k - 1) + (1,), 1),
        ),
        (
            (0, 1, 2) + (0,) * (k - 2) + (1, 0),
            swapPair((0, 1, 2) + (0,) * (k - 2) + (1, 0), 1),
        ),
    )
    # split the a_b_path in 2 at the parallel edge with parallelCycles
    # the cut_node is 1 0^{k} 1 2 - 1 0^{k} 2 1
    # the parallel cut_node is 0 1 0^{k-1} 1 2 - 0 1 0^{k-1} 2 1
    if flip_stutter_cross_edge:
        assert k == 3
        parallel_cut_node = (1, 1) + (0,) * (k - 1) + (2, 0)
        cut_node = swapPair(parallel_cut_node, -3)
        swap_idx = 1
    else:
        cut_node = (0,) * (k - 1) + (1, 2, 1, 0)
        parallel_cut_node = swapPair(cut_node, -3)
        swap_idx = k - 2
    print(
        f"cut_node: {cut_node} and {swapPair(cut_node, swap_idx)}, parallel_cut_node: {parallel_cut_node} and {swapPair(parallel_cut_node, swap_idx)}"
    )
    full = glue(
        c1_c12_c00_c10,
        parallelCycles,
        (cut_node, swapPair(cut_node, swap_idx)),
        (parallel_cut_node, swapPair(parallel_cut_node, swap_idx)),
    )
    return full


def waveTopRowOddOddOne(
    even_odd_1: list[tuple[int, ...]], odd_odd_two_equal: list[tuple[int, ...]]
) -> list[tuple[int, ...]]:
    """
    Connects the even-odd-1 and odd-odd-xx cycles by incorporating the spurs in the zig-zag path.
    This is the top figure of Figure 2.9 of the master thesis document (figure: VerhoeffOdd21);

    Args:
        even_odd_1 (list[tuple[int, ...]]): The even-odd-1 cycle.
        odd_odd_two_equal (list[tuple[int, ...]]): The odd-odd-xx cycle.

    Returns:
        list[tuple[int, ...]]: The connected cycle.

    Raises:
        AssertionError: If the cycle is not a cycle.
        ValueError: If the adjacent nodes are not found in the even-odd-1 cycle.
    """
    # sort the nodes on the indices that the occur in the even_odd_1 cycle while remembering the index
    odd_odd_swapped_with_index = sorted(
        [(node, even_odd_1.index(swapPair(node, -2))) for node in odd_odd_two_equal],
        key=lambda x: -x[1],
    )

    # loop over the nodes in pairs
    for (node1, idx1), (node2, idx2) in zip(*[iter(odd_odd_swapped_with_index)] * 2):
        try:
            assert idx1 - 1 == idx2
        except AssertionError:
            print(f"node1 {node1} at {idx1} and node2 {node2} at {idx2}")
            print(f"even_odd_1: {even_odd_1}")
            raise AssertionError("The nodes are not adjacent")
        # insert the nodes
        even_odd_1 = even_odd_1[:idx1] + [node2, node1] + even_odd_1[idx1:]
    return even_odd_1
