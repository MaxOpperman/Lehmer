from helper_operations.path_operations import (
    createZigZagPath,
    incorporateSpursInZigZag,
    pathQ,
    splitPathIn2,
)
from helper_operations.permutation_graphs import rotate, stutterPermutations, swapPair
from verhoeff import HpathNS


def Hpath_even_1_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from `1 2 0^k` to `0 2 1 0^(k-1)`

    Args:
        k (int): The input value for the number of 0's. Must be odd!

    Returns:
        list[tuple[int, ...]]:
            The generated path from `c` to `d`\n
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
    rotation = 2
    cycle_20_02 = rotate(
        createZigZagPath(cycle_without_stutters, (2, 0), (0, 2)), rotation
    )
    sp02 = stutterPermutations([k, 2])
    cycle_with_stutters = incorporateSpursInZigZag(cycle_20_02, sp02, [(0, 2), (2, 0)])
    return cycle_with_stutters


def incorporated_odd_2_1(k: int) -> list[tuple[int, ...]]:
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
    if k % 2 == 0:
        raise ValueError(f"k must be odd")
    if k == 1:
        return Hpath_odd_2_1(1)
    parallelCycles = parallel_sub_cycle_odd_2_1(k - 1)
    a_b_path = Hpath_odd_2_1(k)
    # split the a_b_path in 2 at the parallel edge with parallelCycles
    cut_node = swapPair(parallelCycles[0], -3)
    split1, split2 = splitPathIn2(a_b_path, cut_node)
    return split1 + parallelCycles + split2
