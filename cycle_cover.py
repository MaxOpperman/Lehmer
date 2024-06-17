import argparse

from helper_operations.path_operations import (
    adjacent,
    conditionHpath,
    createZigZagPath,
    cutCycle,
    cycleQ,
    incorporateSpursInZigZag,
    pathQ,
    splitPathIn2,
    transform,
    transform_cycle_cover,
)
from helper_operations.permutation_graphs import (
    extend,
    extend_cycle_cover,
    multinomial,
    rotate,
    stutterPermutationQ,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma11
from verhoeff import HpathNS


def Hpath(*s) -> list[tuple[int, ...]]:
    """Returns a Hamiltonian path of signature s"""
    if not conditionHpath(s):
        return None
    elif sorted(s, reverse=True) != list(s):
        list_s = list(s)
        list_s.sort(reverse=True)
        return transform(
            Hpath(*list_s),
            [
                i
                for i in sorted(
                    range(len(list_s)), key=lambda x: list_s[x], reverse=True
                )
            ],
        )
    elif s[-1] == 0:
        return Hpath(*s[:-1])
    elif len(s) == 0:
        return []
    elif len(s) == 1:
        return [tuple(list(range(s[0])))]
    elif len(s) == 2 and s[1] == 1:
        return [
            tuple([1 if i == j else 0 for i in range(s[0], -1, -1)])
            for j in range(s[0], -1, -1)
        ]
    else:
        return [tuple(s)]


def HpathAlt(sig: list[int]) -> list[tuple[int, ...]]:
    """
    Generates a path based on the input signature `sig` from 1 2 0^{k0} to 0 2 1 0^{k0-1}.

    Args:
        sig (list[int]): The input signature.

    Returns:
        list[tuple]: The generated path.

    Raises:
        ValueError: If `k0` is not 2, 3, or greater than or equal to 4.
    """
    k0 = sig[0]
    if k0 == 2:
        p2 = extend(Hpath(2, 1, 0), (2,))
        p1 = extend(
            [tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(2, 0, 1)], (1,)
        )
        return (
            [(1, 2, 0, 0), (2, 1, 0, 0), (2, 0, 1, 0)]
            + p1
            + p2[::-1]
            + [(1, 0, 2, 0), (0, 1, 2, 0), (0, 2, 1, 0)]
        )
    elif k0 == 3:
        p2 = extend(Hpath(3, 1, 0), (2,))
        p1 = extend(
            [tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(3, 0, 1)], (1,)
        )
        return (
            [(1, 2, 0, 0, 0), (2, 1, 0, 0, 0), (2, 0, 1, 0, 0), (2, 0, 0, 1, 0)]
            + list(reversed(p1))
            + p2
            + [
                (1, 0, 0, 2, 0),
                (1, 0, 2, 0, 0),
                (0, 1, 2, 0, 0),
                (0, 1, 0, 2, 0),
                (0, 0, 1, 2, 0),
                (0, 0, 2, 1, 0),
                (0, 2, 0, 1, 0),
                (0, 2, 1, 0, 0),
            ]
        )
    elif k0 >= 4:
        p2 = extend(Hpath(k0, 1, 0), (2,))
        p1 = extend(
            [tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(k0, 0, 1)], (1,)
        )
        p20 = extend(Hpath(k0 - 1, 1, 0), (2, 0))
        p10 = extend(
            [tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(k0 - 1, 0, 1)],
            (1, 0),
        )
        # by ind. hyp. a path from 1 2 0^(k-2) to 0 2 1 0^(k-3)
        p00 = extend(HpathAlt(sig[:2] + [sig[2] - 2]), (0, 0))
        return p00[:k0] + [p10[0]] + p1 + p2[::-1] + p20 + p10[1:][::-1] + p00[k0:]
    else:
        raise ValueError("k must be 2, 3 or greater than or equal to 4")


def HpathEven_1_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from 1 2 0^(k) to 0 2 1 0^(k-1)
    @param k: The input value for k0
    @return: The generated path
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


def HpathOdd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from 1 2 0^{k0} 1 to 0 2 1 0^{k0-1} 1.
    @param k: The input value for k0, must be odd
    @return: The generated path from a to b
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


def parallelSubCycleOdd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates the parallel cycle from the 02 and 20 cycles with stutters
    @param k: The input value for k0 (EVEN!) because we don't count the 0 in 02 or 20
    @return: The generated path from 0 1 0^{k-1} 1 0 2 to 1 0^(k) 1 0 2
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


def incorporatedOdd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from 1 2 0^{k0-1} 1 to 0 2 1 0^{k0-2} 1
    Including the _02 and _20 cycles (with stutters), and the _1 & _12 path.

    @param k: The input value for k0, must be odd
    @return: The generated path from a to b
    """
    if k % 2 == 0:
        raise ValueError(f"k must be odd")
    if k == 1:
        return HpathOdd_2_1(1)
    parallelCycles = parallelSubCycleOdd_2_1(k - 1)
    a_b_path = HpathOdd_2_1(k)
    # split the a_b_path in 2 at the parallel edge with parallelCycles
    cut_node = swapPair(parallelCycles[0], -3)
    split1, split2 = splitPathIn2(a_b_path, cut_node)
    return split1 + parallelCycles + split2


def split_node_bool(node: tuple[int, ...], end_tuple: tuple[int, ...]) -> bool:
    """
    Check if the node is a split node based on the end_tuple
    @param node: The node to be checked
    @param end_tuple: The tuple that the node should end with
    @return: True if the node is a split node
    """
    return node[-len(end_tuple) :] == end_tuple and not stutterPermutationQ(
        swapPair(node, -len(end_tuple))
    )


def find_split_node(
    end_tuple: tuple[int, ...], ordered_cycle: list[tuple[int, ...]]
) -> tuple[int, ...]:
    """
    Find the node that splits the cycle in two based on the end_tuple (which is not a stutter permutation)
    @param end_tuple: The tuple that the first split of the cycle should end with
    @param ordered_cycle: The cycle to be split
    @return: The first node in a pair that ends with end_tuple
    """
    split_nodes = [
        node
        for i, node in enumerate(ordered_cycle[:-1])
        if split_node_bool(node, end_tuple)
        and split_node_bool(ordered_cycle[i + 1], end_tuple)
    ]
    # if there is such a split node
    if len(split_nodes) > 0:
        split_node = split_nodes[0]
        print(f"case 1 {split_node}, index {ordered_cycle.index(split_node)}")
    # if no split node is found, it likely is the last node
    elif split_node_bool(ordered_cycle[0], end_tuple) and split_node_bool(
        ordered_cycle[-1], end_tuple
    ):
        split_node = ordered_cycle[-1]
        print(f"case 2 {split_node}, index {len(ordered_cycle)-1}")
    else:
        raise ValueError(
            f"No node found that ends with {end_tuple}\n cycle {ordered_cycle}"
        )
    print(
        f"split node {ordered_cycle[(ordered_cycle.index(split_node)-1)%len(ordered_cycle)]}-{split_node}-{ordered_cycle[(ordered_cycle.index(split_node)+1)%len(ordered_cycle)]} based on {end_tuple} in {ordered_cycle[0]}-{ordered_cycle[-1]}"
    )
    return split_node


def extend_sub_cycle(
    full_cycle_old: list[tuple[int, ...]],
    end_cycle_old: list[tuple[int, ...]],
    end_tuple: tuple[int, ...],
    new_cycle: list[tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Extend the full_cycle and end_cycle with the new_cycle based on the end_tuple
    @param full_cycle_old: The current starting part of the cycle, ends with something adjacent to new_cycle
    @param end_cycle_old: The current ending part of the cycle
    @param end_tuple: The tuple that the the new full_cycle should end with
    @param new_cycle: The new cycle to be added
    @return: The new full_cycle and end_cycle
    """
    print(
        f"old start {full_cycle_old[0]}-{full_cycle_old[-1]}, end tuple {end_tuple}, new cycle {new_cycle[0]}-{new_cycle[-1]}"
    )
    # rotate based on the old starting part of the cycle
    ordered_cycle = cutCycle(new_cycle, swapPair(full_cycle_old[-1], -len(end_tuple)))
    # check if start of full_cycle is adjacent to the new end of ordered_cycle
    if len(end_cycle_old) == 0 and adjacent(full_cycle_old[0], ordered_cycle[1]):
        ordered_cycle = ordered_cycle[:1] + ordered_cycle[1:][::-1]
    elif len(end_cycle_old) > 0 and adjacent(end_cycle_old[0], ordered_cycle[1]):
        ordered_cycle = ordered_cycle[:1] + ordered_cycle[1:][::-1]
    elif (
        len(end_cycle_old) == 0 and not adjacent(full_cycle_old[0], ordered_cycle[-1])
    ) or (len(end_cycle_old) > 0 and not adjacent(end_cycle_old[0], ordered_cycle[-1])):
        print(
            f"ERROR! {full_cycle_old[0]}-{full_cycle_old[-1]} not adjacent to {ordered_cycle[0]}-{ordered_cycle[-1]}"
        )
        raise ValueError("Not adjacent")
    print(
        f"index {swapPair(full_cycle_old[0], -len(end_tuple))}, {ordered_cycle[0]}-{ordered_cycle[-1]}"
    )
    # the split node is the first node of a pair that ends with end_tuple
    split_node = find_split_node(end_tuple, ordered_cycle)
    split_cycle1, split_cycle2 = splitPathIn2(ordered_cycle, split_node)
    if len(end_cycle_old) > 0 and len(split_cycle2) > 0:
        print(
            f"endcycle {end_cycle_old[0]}-{end_cycle_old[-1]}, new end {split_cycle2[0]}-{split_cycle2[-1]} adj {adjacent(end_cycle_old[0], split_cycle2[-1])}"
        )
    else:
        print(
            f"endcycle NO ELEMENTS {end_cycle_old}, new end {split_cycle2}, start {split_cycle1} {full_cycle_old[-1]}"
        )
    full_cycle_old.extend(split_cycle1)
    end_cycle_old = split_cycle2 + end_cycle_old
    return full_cycle_old, end_cycle_old


def HpathCycleCover(sig: list[int]) -> list[list[tuple[int, ...]]]:
    # sort list in descending order
    if len(sig) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(sig) == 1:
        return [[(0,) * sig[0]]]
    sorted_sig = sorted(sig, reverse=True)
    if sorted_sig != sig:
        if sig == [1, 2, 1]:
            return [HpathOdd_2_1(1)]
        indexed_sig = [(value, idx) for idx, value in enumerate(sig)]
        indexed_sig.sort(reverse=True, key=lambda x: x[0])
        return transform_cycle_cover(
            HpathCycleCover(sorted_sig), [x[1] for x in indexed_sig]
        )
    k = sig[0]
    if len(sig) == 2:
        return [HpathNS(sig[0], sig[1])]
    elif 0 in sig:
        return HpathCycleCover(sig[:-1])
    # Odd-1-1 AND Even-1-1 case
    elif len(sig) == 3 and sig[1] == 1 and sig[2] == 1:
        # Split off the trailing number x
        # p_path is k|1 and (after transformation) also k|2
        linear_path = HpathNS(k, 1)
        # a path from 0^k 1 2 to 1 0^k 2
        p2 = extend(linear_path, (2,))
        # a path from 0^k 2 1 to 2 0^k 1
        p1 = extend(
            [tuple(2 if x == 1 else 0 for x in tup) for tup in linear_path], (1,)
        )
        # by IH, a path/cycle from 1 0^k 2 (path to 2 0^k 1)
        p0 = extend(HpathCycleCover([k - 1, 1, 1])[0], (0,))

        # HpathNS is missing a node when k_0 is even, we add this back
        if k % 2 == 0:
            p2 = [tuple([0] * k) + (1, 2)] + p2
            p1 = [tuple([0] * k) + (2, 1)] + p1
        if k == 0:
            # reverse these, because sorting of signature reversed up the order
            p1 = p1[::-1]
            p0 = p0[::-1]

        if k % 2 == 1:
            return [p2[-1:] + p0 + p1[::-1] + p2[:-1]]
        else:
            # Even k, also need to add 0^k0 1 2 and 0^k0 2 1
            return [p2[-1:] + p0 + p2[:-1][::-1] + p1]
    # even-2-1 case
    elif len(sig) == 3 and k % 2 == 0 and sig[1] == 2 and sig[2] == 1:
        p2 = extend(HpathNS(k, 2), (2,))  # a cycle from 1 0^k 1 2 to 1 0 1 0^(k-1) 2
        p1 = extend(
            HpathEven_1_1(k),
            (1,),
        )  # a path from c = 1 2 0^k 1 to d = 0 2 1 0^(k-1) 1
        p0 = extend(
            HpathCycleCover([k - 1, 2, 1])[0][::-1], (0,)
        )  # a path from b0 = 0 2 1 0^(k-2) 1 0 to a0 = 1 2 0^(k-1) 1 0
        # 1 2 0^{k2} to 0 2 1 0^{k2-1}.
        v = (1,) + tuple([0] * k) + (1, 2)
        c = p0 + p1
        return [cutCycle(p2, swapPair(v, 1))[::-1] + cutCycle(c, swapPair(v, -2))]
    # odd-2-1 case
    elif len(sig) == 3 and k % 2 == 1 and sig[1] == 2 and sig[2] == 1:
        # the path from a to b (_1 | _12) with parallel 02-20 cycles incorporated
        p1_p12_p02_p20 = incorporatedOdd_2_1(k)
        # path from c'10=120^{k_0-1}10 to d'10=0210^{k_0-1}10 (_10)
        p10 = extend(HpathEven_1_1(k - 1), (1, 0))
        # path from a'00=120^{k_0-2}100 to b'00=0210^{k_0-3}100 (_00)
        p00 = extend(HpathCycleCover([k - 2, 2, 1])[0], (0, 0))
        cycle = rotate(p10 + p00[::-1], 1)[::-1]
        # b = 0 2 1 0^(k-2) 1 to a = 1 2 0^(k-1) 1
        return [p1_p12_p02_p20[:1] + cycle + p1_p12_p02_p20[1:]]
    # stachowiak's odd case
    elif sum(1 for n in sig if n % 2 == 1) >= 2:
        # index the numbers in the signature such that we can transform them back later
        indexed_sig = [(value, idx) for idx, value in enumerate(sig)]
        # put the odd numbers first in the signature
        indexed_sig.sort(reverse=True, key=lambda x: [x[0] % 2, x[0]])
        return [
            transform(lemma11([x[0] for x in indexed_sig]), [x[1] for x in indexed_sig])
        ]
    # all-but-one even case
    elif any(n % 2 == 1 for n in sig):
        all_sub_cycles = []
        for idx, color in enumerate(sig):
            sub_sig = sig[:idx] + [color - 1] + sig[idx + 1 :]
            # check if this results an odd-2-1 case, then we need a cycle and not a path
            indexed_sub_sig = [(value, idx) for idx, value in enumerate(sub_sig)]
            indexed_sub_sig.sort(reverse=True, key=lambda x: [x[0] % 2, x[0]])
            sorted_sub_sig = [x[0] for x in indexed_sub_sig]
            if (
                sorted_sub_sig[0] % 2 == 1
                and sorted_sub_sig[1] == 1
                and sorted_sub_sig[2] == 2
            ):
                c = [
                    transform(lemma11(sorted_sub_sig), [x[1] for x in indexed_sub_sig])
                ]
            else:
                c = HpathCycleCover(sub_sig)
            all_sub_cycles.append(extend_cycle_cover(c, (idx,)))
        return all_sub_cycles
    # all-even case
    else:
        all_sub_cycles = []
        for idx, color in enumerate(sig):
            temp_sig = sig[:idx] + [color - 1] + sig[idx + 1 :]
            for idx2, second_color in enumerate(temp_sig[idx:], start=idx):
                sub_sig = temp_sig[:idx2] + [second_color - 1] + temp_sig[idx2 + 1 :]
                # check if this results an even-1-1 case
                sorted_sub_sig = sorted(sub_sig, reverse=True)
                indexed_sub_sig = [(value, idx) for idx, value in enumerate(sub_sig)]
                indexed_sub_sig.sort(reverse=True, key=lambda x: x[0])
                # for the even-1-1 case we need a specific path that has parallel edges
                if (
                    sorted_sub_sig[0] % 2 == 0
                    and sorted_sub_sig[1] == 1
                    and sorted_sub_sig[2] == 1
                ):
                    cycle_cover = [
                        transform(
                            HpathEven_1_1(sorted_sub_sig[0]),
                            [x[1] for x in indexed_sub_sig],
                        )
                    ]
                else:
                    cycle_cover = HpathCycleCover(sub_sig)
                if idx != idx2:
                    # this gives two parallel paths which we need to combine into a cycle
                    sub_cycles = []
                    for cyc in cycle_cover:
                        sub_cycles.append(
                            extend(cyc, (idx2, idx))[::-1] + extend(cyc, (idx, idx2))
                        )
                else:
                    # this gives all the non-stutter permutations
                    sub_cycles = extend_cycle_cover(cycle_cover, (idx, idx2))
                all_sub_cycles.append(sub_cycles)
        return all_sub_cycles


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
    s = [int(x) for x in args.signature.split(",")]
    if len(s) > 1:
        perms = HpathCycleCover(s)
        if args.verbose:
            print(f"Resulting path {perms}")
        stut_count = len(stutterPermutations(s))
        print(
            f"Verhoeff's result for signature {s}: {len(set(tuple(row) for row in perms))}/{len(perms)}/{multinomial(s)} "
            f"(incl {stut_count} stutters {stut_count+len(perms)}) is a path: {pathQ(perms)} and a cycle: {cycleQ(perms)}"
        )
