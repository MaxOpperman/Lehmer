from helper_operations.cycle_cover_connections import filter_adjacent_edges_by_tail
from helper_operations.path_operations import (
    adjacent,
    createZigZagPath,
    cutCycle,
    cycleQ,
    glue,
    incorporateSpurInZigZag,
    incorporateSpursInZigZag,
    pathQ,
    splitPathIn2,
    spurBaseIndex,
    stutterPermutationQ,
    transform,
)
from helper_operations.permutation_graphs import (
    extend,
    get_perm_signature,
    rotate,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma2_extended_path
from verhoeff import HpathNS


def Hpath_even_1_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from `1 2 0^k` to `0 2 1 0^(k-1)`

    Args:
        k (int): The input value for the number of 0's. Must be even!

    Returns:
        list[tuple[int, ...]]:
            The generated path from `c` to `d`:
            - `c = 1 2 0^k`
            - `d = 0 2 1 0^(k-1)`

    Raises:
        ValueError: If `k` is not even
    """
    if k % 2 == 1:
        raise ValueError("k must be even")
    if k == 2:
        path = [
            (1, 2, 0, 0),
            (2, 1, 0, 0),
            (2, 0, 1, 0),
            (2, 0, 0, 1),
            (0, 2, 0, 1),
            (0, 0, 2, 1),
            (0, 0, 1, 2),
            (0, 1, 0, 2),
            (1, 0, 0, 2),
            (1, 0, 2, 0),
            (0, 1, 2, 0),
            (0, 2, 1, 0),
        ]
        assert pathQ(path)
        return path
    k_0_tuple = tuple([0] * k)
    bottom_path = [
        (1, 2) + k_0_tuple,
    ]
    # construct the path on the bottom, incl the bottom-right corner node
    for i in range(0, k + 1):
        bottom_path.append((2,) + k_0_tuple[:i] + (1,) + k_0_tuple[i:])
    midpath = []
    for i in range(0, k, 2):
        # construct the path going up
        up_path = (0,) + k_0_tuple[i + 1 :] + (1,) + k_0_tuple[1 : i + 1]
        for j in range(1, len(up_path) - i):
            midpath.append(up_path[:j] + (2,) + up_path[j:])
        # construct the path going left (incl top-right corner node)
        left_path = k_0_tuple[i:] + (2,) + k_0_tuple[:i]
        for j in reversed(range(0, len(left_path) - i)):
            midpath.append(left_path[:j] + (1,) + left_path[j:])
        right_path = k_0_tuple[i + 1 :] + (2,) + k_0_tuple[: i + 1]
        # construct the path going right (incl top-right corner node)
        for j in range(0, len(right_path) - i):
            midpath.append(right_path[:j] + (1,) + right_path[j:])
        # construct the path going down
        down_path = k_0_tuple[i + 1 :] + (1,) + k_0_tuple[: i + 1]
        for j in reversed(range(1, len(down_path) - 2 - i)):
            midpath.append(down_path[:j] + (2,) + down_path[j:])
    return bottom_path + midpath


def Hpath_odd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from `1 2 0^{k0} 1` to `0 2 1 0^{k0-1} 1`.

    Args:
        k (int): The input value for the number of 0's. Must be odd!

    Returns:
        list[tuple[int, ...]]:
            The generated path from `a` to `b`\n
            - `a = 1 2 0^{k0} 1`
            - `b = 0 2 1 0^{k0-1} 1`

    Raises:
        ValueError: If `k` is not odd
    """
    if k % 2 == 0:
        raise ValueError("k must be odd")
    if k == 1:
        # base case
        path = [
            (1, 2, 0, 1),
            (1, 0, 2, 1),
            (0, 1, 2, 1),
            (0, 1, 1, 2),
            (1, 0, 1, 2),
            (1, 1, 0, 2),
            (1, 1, 2, 0),
            (1, 2, 1, 0),
            (2, 1, 1, 0),
            (2, 1, 0, 1),
            (2, 0, 1, 1),
            (0, 2, 1, 1),
        ]
        assert pathQ(path)
        return path
    k_0_tuple = tuple([0] * k)
    start_path = [(1, 2) + k_0_tuple + (1,)]
    bottom_path = (2,) + k_0_tuple + (1,)
    for i in range(1, len(bottom_path)):
        start_path.append(bottom_path[:i] + (1,) + bottom_path[i:])
    if k > 3:
        end_path_1 = [
            (0, 2, 0, 0, 1) + k_0_tuple[:-3] + (1,),
            (0, 0, 2, 0, 1) + k_0_tuple[:-3] + (1,),
            (0, 0, 0, 2, 1) + k_0_tuple[:-3] + (1,),
            (0, 0, 0, 1, 2) + k_0_tuple[:-3] + (1,),
            (0, 0, 0, 1, 0, 2) + k_0_tuple[:-4] + (1,),
            (0, 0, 1, 0, 0, 2) + k_0_tuple[:-4] + (1,),
            (0, 1, 0, 0, 0, 2) + k_0_tuple[:-4] + (1,),
            (1, 0, 0, 0, 0, 2) + k_0_tuple[:-4] + (1,),
        ]
        mid_path = []
        for i in range(3, k, 2):
            prefix_zeros = i - 3
            for j in range(1, k + 1 - prefix_zeros):
                mid_path.append(
                    k_0_tuple[:j]
                    + (2,)
                    + k_0_tuple[j : k - prefix_zeros]
                    + (1,)
                    + k_0_tuple[:prefix_zeros]
                    + (1,)
                )
            mid_path.append(
                k_0_tuple[prefix_zeros:] + (1, 2) + k_0_tuple[:prefix_zeros] + (1,)
            )
            if prefix_zeros == 0:
                for j in range(0, k + 1):
                    mid_path.append(k_0_tuple[j:] + (1,) + k_0_tuple[:j] + (1, 2))
                for j in range(0, k):
                    mid_path.append(
                        k_0_tuple[:prefix_zeros]
                        + k_0_tuple[:j]
                        + (1,)
                        + k_0_tuple[j:]
                        + (2, 1)
                    )
            else:
                for j in range(0, k - prefix_zeros + 1):
                    mid_path.append(
                        k_0_tuple[j + prefix_zeros :]
                        + (1,)
                        + k_0_tuple[: j + 1]
                        + (2,)
                        + k_0_tuple[: prefix_zeros - 1]
                        + (1,)
                    )
                for j in reversed(range(1, k - prefix_zeros + 1)):
                    mid_path.append(
                        k_0_tuple[j + prefix_zeros :]
                        + (1,)
                        + k_0_tuple[:j]
                        + (2,)
                        + k_0_tuple[:prefix_zeros]
                        + (1,)
                    )
            temp = (
                k_0_tuple[: k - 1 - prefix_zeros]
                + (1,)
                + k_0_tuple[-1 - prefix_zeros :]
                + (1,)
            )
            for j in reversed(range(1, len(temp) - 1 - prefix_zeros)):
                mid_path.append(temp[:j] + (2,) + temp[j:])
    else:
        end_path_1 = [
            (0, 2, 0, 0, 1, 1),
            (0, 0, 2, 0, 1, 1),
            (0, 0, 0, 2, 1, 1),
            (0, 0, 0, 1, 2, 1),
            (0, 0, 0, 1, 1, 2),
            (0, 0, 1, 0, 1, 2),
            (0, 1, 0, 0, 1, 2),
            (1, 0, 0, 0, 1, 2),
        ]
        mid_path = []
    end_path_2 = [
        (1, 0, 0, 0, 2) + k_0_tuple[:-3] + (1,),
        (1, 0, 0, 2) + k_0_tuple[:-2] + (1,),
        (1, 0, 2) + k_0_tuple[:-1] + (1,),
        (0, 1, 2, 0, 0) + k_0_tuple[:-3] + (1,),
        (0, 1, 0, 2, 0) + k_0_tuple[:-3] + (1,),
        (0, 1, 0, 0, 2) + k_0_tuple[:-3] + (1,),
        (0, 0, 1, 0, 2) + k_0_tuple[:-3] + (1,),
        (0, 0, 1, 2, 0) + k_0_tuple[:-3] + (1,),
        (0, 0, 2, 1, 0) + k_0_tuple[:-3] + (1,),
        (0, 2, 0, 1, 0) + k_0_tuple[:-3] + (1,),
        (0, 2, 1, 0, 0) + k_0_tuple[:-3] + (1,),
    ]
    assert pathQ(start_path + mid_path + end_path_1 + end_path_2)
    return start_path + mid_path + end_path_1 + end_path_2


def Hcycle_odd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a cycle based on the number of 0's `k` from `1 0 2 0^{k0-1} 1` to `0 1 2 0^{k0-1} 1`.

    Args:
        k (int): The input value for the number of 0's. Must be odd!

    Returns:
        list[tuple[int, ...]]:
            The generated cycle from `e` to `f`\n
            - `e = 1 0 2 0^{k0-1} 1`
            - `f = 0 1 2 0^{k0-1} 1`

    Raises:
        ValueError: If `k` is not odd or k < 3
    """
    if k % 2 == 0:
        raise ValueError(f"k must be odd, got {k}")
    if k < 3:
        raise ValueError(
            "k must be greater than 1, use Hpath_odd_2_1(1) instead for k=1"
        )
    k_0_tuple = tuple([0] * k)
    start_cycle = [(1, 0, 2) + k_0_tuple[:-1] + (1,), (1, 2) + k_0_tuple + (1,)]
    bottom_cycle = (2,) + k_0_tuple + (1,)
    for i in range(1, len(bottom_cycle)):
        start_cycle.append(bottom_cycle[:i] + (1,) + bottom_cycle[i:])
    if k > 3:
        end_cycle_1 = [
            (0, 2, 0, 0, 1) + k_0_tuple[:-3] + (1,),
            (0, 0, 2, 0, 1) + k_0_tuple[:-3] + (1,),
            (0, 0, 0, 2, 1) + k_0_tuple[:-3] + (1,),
            (0, 0, 0, 1, 2) + k_0_tuple[:-3] + (1,),
            (0, 0, 0, 1, 0, 2) + k_0_tuple[:-4] + (1,),
            (0, 0, 1, 0, 0, 2) + k_0_tuple[:-4] + (1,),
            (0, 1, 0, 0, 0, 2) + k_0_tuple[:-4] + (1,),
            (1, 0, 0, 0, 0, 2) + k_0_tuple[:-4] + (1,),
        ]
        mid_cycle = []
        for i in range(3, k, 2):
            prefix_zeros = i - 3
            for j in range(1, k + 1 - prefix_zeros):
                mid_cycle.append(
                    k_0_tuple[:j]
                    + (2,)
                    + k_0_tuple[j : k - prefix_zeros]
                    + (1,)
                    + k_0_tuple[:prefix_zeros]
                    + (1,)
                )
            mid_cycle.append(
                k_0_tuple[prefix_zeros:] + (1, 2) + k_0_tuple[:prefix_zeros] + (1,)
            )
            if prefix_zeros == 0:
                for j in range(0, k + 1):
                    mid_cycle.append(k_0_tuple[j:] + (1,) + k_0_tuple[:j] + (1, 2))
                for j in range(0, k):
                    mid_cycle.append(
                        k_0_tuple[:prefix_zeros]
                        + k_0_tuple[:j]
                        + (1,)
                        + k_0_tuple[j:]
                        + (2, 1)
                    )
            else:
                for j in range(0, k - prefix_zeros + 1):
                    mid_cycle.append(
                        k_0_tuple[j + prefix_zeros :]
                        + (1,)
                        + k_0_tuple[: j + 1]
                        + (2,)
                        + k_0_tuple[: prefix_zeros - 1]
                        + (1,)
                    )
                for j in reversed(range(1, k - prefix_zeros + 1)):
                    mid_cycle.append(
                        k_0_tuple[j + prefix_zeros :]
                        + (1,)
                        + k_0_tuple[:j]
                        + (2,)
                        + k_0_tuple[:prefix_zeros]
                        + (1,)
                    )
            temp = (
                k_0_tuple[: k - 1 - prefix_zeros]
                + (1,)
                + k_0_tuple[-1 - prefix_zeros :]
                + (1,)
            )
            for j in reversed(range(1, len(temp) - 1 - prefix_zeros)):
                mid_cycle.append(temp[:j] + (2,) + temp[j:])
    else:
        end_cycle_1 = [
            (0, 2, 0, 0, 1, 1),
            (0, 0, 2, 0, 1, 1),
            (0, 0, 0, 2, 1, 1),
            (0, 0, 0, 1, 2, 1),
            (0, 0, 0, 1, 1, 2),
            (0, 0, 1, 0, 1, 2),
            (0, 1, 0, 0, 1, 2),
            (1, 0, 0, 0, 1, 2),
        ]
        mid_cycle = []
    end_cycle_2 = [
        (1, 0, 0, 0, 2) + k_0_tuple[:-3] + (1,),
        (1, 0, 0, 2) + k_0_tuple[:-2] + (1,),
        (0, 1, 0, 2, 0) + k_0_tuple[:-3] + (1,),
        (0, 1, 0, 0, 2) + k_0_tuple[:-3] + (1,),
        (0, 0, 1, 0, 2) + k_0_tuple[:-3] + (1,),
        (0, 0, 1, 2, 0) + k_0_tuple[:-3] + (1,),
        (0, 0, 2, 1, 0) + k_0_tuple[:-3] + (1,),
        (0, 2, 0, 1, 0) + k_0_tuple[:-3] + (1,),
        (0, 2, 1, 0, 0) + k_0_tuple[:-3] + (1,),
        (0, 1, 2, 0, 0) + k_0_tuple[:-3] + (1,),
    ]
    assert pathQ(start_cycle + mid_cycle + end_cycle_1 + end_cycle_2)
    return start_cycle + mid_cycle + end_cycle_1 + end_cycle_2


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


def incorporated_odd_2_1_cycle(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from `e = 1 0 2 0^{k0-1} 1` to `f = 0 1 2 0^{k0-1} 1`.
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
    # split the a_b_path in 2 at the parallel edge with parallelCycles
    # the cut_node is 0^2 1 0^{k-2} 1 2 and 0^3 1 0^{k-3} 1 2
    cut_node = (0,) * (k - 1) + (1, 0, 1, 2)
    parallel_cut_node = swapPair(cut_node, -3)
    p1_p12_p02_p20 = glue(
        e_f_cylce,
        parallelCycles,
        (cut_node, swapPair(cut_node, k - 2)),
        (parallel_cut_node, swapPair(parallel_cut_node, k - 2)),
    )

    # path from c'10=120^{k_0-1}10 to d'10=0210^{k_0-1}10 (_10)
    p10 = extend(Hpath_even_1_1(k - 1), (1, 0))
    # path from a'00=120^{k_0-2}100 to b'00=0210^{k_0-3}100 (_00)
    p00 = extend(incorporated_odd_2_1_path_a_b(k - 2), (0, 0))

    # generate the cycle from c=1 2 0^{k0-1} 1 0 to 2 1 0^{k0-1} 1 0
    cycle = p10 + p00[::-1]
    assert cycleQ(cycle)
    # split the cycle in two at the node 1 2 0^{k0} 1 - 2 1 0^{k0} 1
    full = glue(
        p1_p12_p02_p20,
        cycle,
        ((1, 2) + (0,) * k + (1,), swapPair((1, 2) + (0,) * k + (1,), 0)),
        (
            (1, 2) + (0,) * (k - 1) + (1, 0),
            swapPair((1, 2) + (0,) * (k - 1) + (1, 0), 0),
        ),
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
