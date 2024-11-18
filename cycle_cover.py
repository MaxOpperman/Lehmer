import argparse
from functools import cache

from helper_operations.cycle_cover_connections import (
    connect_single_cycle_cover,
    generate_end_tuple_order,
    get_tail_length,
)
from helper_operations.cycle_cover_generation import (
    Hpath_even_1_1,
    Hpath_odd_2_1,
    incorporated_odd_2_1_cycle,
    incorporated_odd_2_1_path_a_b,
    waveTopRowOddOddOne,
)
from helper_operations.path_operations import (
    adjacent,
    createZigZagPath,
    cutCycle,
    cycleQ,
    get_first_element,
    get_transformer,
    glue,
    pathQ,
    recursive_cycle_check,
    spurBaseIndex,
    transform,
    transform_cycle_cover,
)
from helper_operations.permutation_graphs import (
    extend,
    extend_cycle_cover,
    get_perm_signature,
    incorporateSpursInZigZag,
    multinomial,
    nonStutterPermutations,
    perm,
    rotate,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma2_extended_path
from verhoeff import HpathNS


def add_cycle_in_order(
    cycle_cover: list[list[tuple[int, ...]]],
    cycle: list[list[tuple[int, ...]]],
    cycle_end: tuple[int, int],
) -> list[list[tuple[int, ...]]]:
    """
    Adds a cycle to the cycle cover in order. The order is based on the last two elements of the cycle.
    The last element should be the smallest and then the second to last element should be the smallest.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to add the cycle to. The depth of the list is undefined and depends on the cycle cover.
        cycle (list[list[tuple[int, ...]]]): The cycle to add.
        cycle_end (tuple[int, int]): The last two elements of the cycle. The last element should be the largest.

    Returns:
        list[list[tuple[int, ...]]]: The cycle cover with the added cycle.

    Raises:
        AssertionError: If the cycle is empty.
    """
    assert len(cycle) > 0
    if len(cycle_cover) == 0:
        return [cycle]
    last_element = cycle_end[1]
    second_last_element = cycle_end[0]
    for idx, c in enumerate(cycle_cover):
        # get the tuple
        perm_list = get_first_element(c)
        # sort the last two elements from small to large
        old_last_element = max(perm_list[-1], perm_list[-2])
        old_second_last_element = min(perm_list[-1], perm_list[-2])
        # if the last element is less than the old last element, prepend it
        if last_element < old_last_element:
            cycle_cover.insert(idx, cycle)
            return cycle_cover
        # if the last element is equal to the old last element, check the second last element
        elif (
            old_last_element == last_element
            and second_last_element < old_second_last_element
        ):
            cycle_cover.insert(idx, cycle)
            return cycle_cover
    # if the new cycle is larger than all the old cycles, append it
    cycle_cover.append(cycle)
    return cycle_cover


def generate_all_even_cycle_cover(sig: tuple[int, ...]) -> list[list[tuple[int, ...]]]:
    """
    Generates the disjoint cycle cover on the non-stutter permutations for the given signature `sig` according to the Theorem by Verhoeff.\n
    **Theorem:** *When the arity is at least 3 and at most one k i is odd, the neighbor-swap graph
    of non-stutter permutations admits a disjoint cycle cover, that is, a set of vertex-disjoint
    cycles that visit all permutations exactly once.*\n
    This handles the case where all elements are even. This is done by fixing the trailing two elements and then generating the cycle cover for the remaining signature.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must have at least one element.

    Returns:
        list[list[tuple[int, ...]]]:
            The cycle cover for the given signature `sig`.\n
            Every list of tuples is a cycle in the cycle cover. The tuples are permutations.
            The lists do not have a defined depth since they can consist of cycle covers themselves. But the depth is at least 2.
    """
    all_sub_cycles = []
    between_cycles = []
    for idx, color in enumerate(sig):
        temp_sig = sig[:idx] + (color - 1,) + sig[idx + 1 :]
        for idx2, second_color in enumerate(temp_sig[idx:], start=idx):
            sub_sig = temp_sig[:idx2] + (second_color - 1,) + temp_sig[idx2 + 1 :]
            # check if this results an even-1-1 case
            sorted_sub_sig, transformer2 = get_transformer(sub_sig, lambda x: x[0])
            # for the even-1-1 case we need a specific path that has parallel edges
            if (
                len(list(sorted_sub_sig)) == 3
                and sorted_sub_sig[0] % 2 == 0
                and sorted_sub_sig[1] == 1
                and sorted_sub_sig[2] == 1
            ):
                cycle_cover = [
                    transform(
                        Hpath_even_1_1(sorted_sub_sig[0]),
                        transformer2,
                    )
                ]
            else:
                cycle_cover = generate_cycle_cover(sub_sig)
            if idx != idx2:
                # this gives a set of cycles that we just need to add in order
                sub_cycles = []
                if len(cycle_cover) == 1:
                    sub_cycles.append(
                        extend(cycle_cover[0], (idx2, idx))[::-1]
                        + extend(cycle_cover[0], (idx, idx2))
                    )
                else:
                    # first connect them, then add them
                    connected = get_connected_cycle_cover(sub_sig)
                    sub_cycles = [
                        extend(connected, (idx2, idx))[::-1]
                        + extend(connected, (idx, idx2))
                    ]
                if idx2 - idx <= 1:
                    all_sub_cycles.append(sub_cycles)
                else:
                    between_cycles = add_cycle_in_order(
                        between_cycles, sub_cycles, (idx, idx2)
                    )
            else:
                # this gives all the non-stutter permutations
                sub_cycles = extend_cycle_cover(cycle_cover, (idx, idx2))
                all_sub_cycles.append(sub_cycles)
                if len(sub_sig) == idx + 1:
                    # add the between cycles in reversed order
                    while (
                        len(between_cycles) > 0
                        and idx == max(get_first_element(between_cycles)[-2:])
                        and max(get_first_element(between_cycles, -1)[-2:]) == idx
                    ):
                        all_sub_cycles.append(between_cycles.pop(-1))
                else:
                    # add the between cycles in normal order
                    while len(between_cycles) > 0 and idx == max(
                        get_first_element(between_cycles)[-2:]
                    ):
                        all_sub_cycles.append(between_cycles.pop(0))
    if len(between_cycles) > 0:
        all_sub_cycles.append(between_cycles.pop(0))
    return all_sub_cycles


@cache
def odd_odd_1_cycle(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generates a cycle for the odd-odd-1 case. It uses the waveTopRowOddOddOne function to transform the odd-odd subcase into a cycle.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must be of structure odd-odd-1.

    Returns:
        list[tuple[int, ...]]: The cycle for the odd-odd-1 case.
    """
    # easy first; odd-even-1 and even-odd-1
    even_odd_x = extend(get_connected_cycle_cover((sig[0] - 1, sig[1], 1)), (0,))
    odd_even_y = extend(get_connected_cycle_cover((sig[0], sig[1] - 1, 1)), (1,))

    # now we have the odd-odd part which splits in a few parts with even-even
    even_even_cxy2 = HpathNS(sig[0] - 1, sig[1] - 1)
    # because the XY makes it two parallel and isomorphic cycles, they are combined into one cycle
    odd_odd_zigzag = createZigZagPath(even_even_cxy2, (0, 1), (1, 0))
    even_even_stutter_perms = stutterPermutations((sig[0] - 1, sig[1] - 1))
    odd_odd_cycle = incorporateSpursInZigZag(
        odd_odd_zigzag,
        even_even_stutter_perms,
        [(1, 0), (0, 1)],
    )
    extended_odd_odd = [extend(odd_odd_cycle, (2,))]
    # now the XX and YY parts are still missing, by induction they also contain a cycle
    odd_odd_xx2 = extend(HpathNS(sig[0] - 2, sig[1]), (0, 0, 2))
    odd_odd_yy2 = extend(HpathNS(sig[0], sig[1] - 2), (1, 1, 2))
    even_odd_cut = waveTopRowOddOddOne(even_odd_x, odd_odd_xx2)
    odd_even_cut = waveTopRowOddOddOne(odd_even_y, odd_odd_yy2)

    # the cut nodes are 1 2 1^{k1-1} 0^{k0-2} 0 and 2 1 1^{k1-1} 0^{k0-2} 0
    even_odd_cut_node = (1, 2) + (1,) * (sig[1] - 2) + (0,) * (sig[0] - 1) + (1, 0)
    odd_even_cut_node = swapPair(even_odd_cut_node, -2)
    print(
        f"cut nodes {even_odd_cut_node}-{swapPair(even_odd_cut_node, 0)} and {odd_even_cut_node}-{swapPair(odd_even_cut_node, 0)}"
    )
    even_odd_combined = glue(
        even_odd_cut,
        odd_even_cut,
        (even_odd_cut_node, swapPair(even_odd_cut_node, 0)),
        (odd_even_cut_node, swapPair(odd_even_cut_node, 0)),
    )
    assert cycleQ(even_odd_combined)
    # the cut nodes are 0^{k0-1} 1^{k1} 2 0 and 0 ^{k0-2} 1 0 1^{k1-1} 2 0
    extended_odd_odd_cut_node = (1,) * (sig[1] - 1) + (0,) * (sig[0]) + (1, 2)
    combined_cut_node = swapPair(extended_odd_odd_cut_node, -2)

    result = glue(
        even_odd_combined,
        extended_odd_odd[0],
        (combined_cut_node, swapPair(combined_cut_node, sig[1] - 2)),
        (
            extended_odd_odd_cut_node,
            swapPair(extended_odd_odd_cut_node, sig[1] - 2),
        ),
    )

    return [result]


def even_2_1_cycle(
    k: int,
) -> list[tuple[int, ...]]:
    """
    Generates a Hamiltonian cycle for the even-2-1 case.

    Args:
        k (int): Value for `even` or `k_0`.

    Returns:
        list[tuple[int, ...]]: The cycle for the even-odd-1 case.
    """
    # a cycle from 1 0^(k-1) 1 0 2 to 1 0^k 1 2
    p2 = extend(HpathNS(k, 2), (2,))[::-1]

    # p0 and p1 are combined into a cycle
    # a path from c1 = 1 2 0^k 1 to d1 = 0 2 1 0^(k-1) 1
    p1 = extend(Hpath_even_1_1(k), (1,))
    # a path from b0 = 0 2 1 0^(k-2) 1 0 to a0 = 1 2 0^(k-1) 1 0
    p0 = extend(incorporated_odd_2_1_path_a_b(k - 1)[::-1], (0,))

    # v = 1 0^(k-1) 1 2
    v = (1,) + tuple([0] * k) + (1, 2)
    c = p0 + p1
    return [cutCycle(p2, swapPair(v, 1))[::-1] + cutCycle(c, swapPair(v, -2))]


@cache
def even_odd_1_cycle(
    sig: tuple[int, ...], distinct_ends: bool = True
) -> list[tuple[int, ...]]:
    """
    Generates a cycle for the even-odd-1 case. This is a cycle that contains two parallel cycles that are isomorphic to each other.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must be of structure even-odd-1 or odd-even-1.
        distinct_ends (bool, optional): If the ends of the cutnodes should be distinct. Defaults to True.

    Returns:
        list[tuple[int, ...]]: The cycle for the even-odd-1 case.
    """
    # find the even and odd elements
    even_idx = next(i for i, v in enumerate(sig) if v % 2 == 0)
    odd_idx = 1 if even_idx == 0 else 0
    # odd-1, even, 1 (appended with even); so even, even, 1
    odd_odd_1 = extend(
        get_connected_cycle_cover(
            (
                sig[0] - (1 if sig[0] % 2 == 0 else 0),
                sig[1] - (1 if sig[1] % 2 == 0 else 0),
                1,
            )
        ),
        (even_idx,),
    )

    # even, odd, 1 (appended with both even and odd, since both subtracted by 1; smaller case holds by induction)
    even_odd_x = extend(
        get_connected_cycle_cover((sig[0] - 1, sig[1] - 1, 1)), (even_idx, odd_idx)
    )

    # odd-2, even, 1 (appended with odd, odd); so odd, even, 1 (but a smaller case)
    odd_even_y = extend(
        get_connected_cycle_cover(
            (sig[0] - (sig[0] % 2) * 2, sig[1] - (sig[1] % 2) * 2, 1)
        ),
        (odd_idx, odd_idx),
    )

    # odd, even-1 (appended with even, 2); so a path: odd, odd
    odd_odd_p2 = extend(
        HpathNS(
            sig[0] - (1 if sig[0] % 2 == 0 else 0),
            sig[1] - (1 if sig[1] % 2 == 0 else 0),
        ),
        (even_idx, 2),
    )

    # now we have the even-odd part which splits into odd-odd and even-even
    even_even_cycle = HpathNS(sig[0] - (sig[0] % 2), sig[1] - (sig[1] % 2))

    # rotate the path to a spur base index
    even_even_stutter_perms = stutterPermutations(
        (sig[0] - (sig[0] % 2), sig[1] - (sig[1] % 2))
    )
    # the spur base index - 1 rotates the path to the be one node before the spur base
    even_even_cycle_rotated = rotate(
        even_even_cycle,
        spurBaseIndex(even_even_cycle, even_even_stutter_perms[0]) - 1,
    )

    even_even_c2odd_odd2 = createZigZagPath(
        even_even_cycle_rotated,
        (2, odd_idx),
        (odd_idx, 2),
    )
    # odd-1, even (appended with odd, 2 and 2, odd) and stutters incorporated; so even, even
    incorporated_even_even = incorporateSpursInZigZag(
        even_even_c2odd_odd2,
        even_even_stutter_perms,
        [(odd_idx, 2), (2, odd_idx)],
    )

    if sig[odd_idx] - 2 == 1:
        # for even-1-1 signature, we need to change the path to a cycle
        odd_even_1_tip, odd_even_y = odd_even_y[:2], odd_even_y[2:]
        # the tip is 12 0^k 11 - 21 0^k 11
        # cut the cycle to a vertex adjacent to the tip
        even_odd_cut = cutCycle(even_odd_x, swapPair(odd_even_1_tip[0], -3))
        if even_odd_cut[1] != swapPair(odd_even_1_tip[1], -3):
            # make sure the second vertex is adjacent to the second vertex of the tip
            even_odd_cut = even_odd_cut[:1] + even_odd_cut[1:][::-1]
        # move the tip between the two adjacent vertices
        even_odd_x = even_odd_cut[:1] + odd_even_1_tip + even_odd_cut[1:]

    # assume even is 0 and odd is 1
    # 0^{k0-1} 21^{k1-2} 011 and 0^{k0-2} 201^{k1-2} 011
    cn_011 = (
        (even_idx,) * (sig[even_idx] - 1)
        + (2,)
        + (odd_idx,) * (sig[odd_idx] - 2)
        + (even_idx, odd_idx, odd_idx)
    )
    # 0^{k0-1} 21^{k1-2} 101 and 0^{k0-2} 201^{k1-2} 101
    cn_101 = swapPair(cn_011, -3)
    swapidx_cn_101_011 = sig[even_idx] - 2
    print(
        f"gluing x and y between {cn_011}-{swapPair(cn_011, swapidx_cn_101_011)} and {cn_101}-{swapPair(cn_101, swapidx_cn_101_011)}"
    )
    c_01_11 = glue(
        odd_even_y,
        even_odd_x,
        (cn_011, swapPair(cn_011, swapidx_cn_101_011)),
        (cn_101, swapPair(cn_101, swapidx_cn_101_011)),
    )
    if distinct_ends:
        # 0^{k0} 1^{k1-1} 2 1 and 0^{k0-1} 10 1^{k1-2} 2 1
        cn_021 = (
            (even_idx,) * (sig[even_idx])
            + (odd_idx,) * (sig[odd_idx] - 1)
            + (2, odd_idx)
        )
        # 0^{k0} 1^{k1-2} 2 11 and 0^{k0-1} 10 1^{k1-3} 2 11
        cn_201 = swapPair(cn_021, -3)
        swapidx = sig[even_idx] - 1
    else:
        # 1^{k1-1} 0^{k0} 2 1 and 1^{k1-2} 01 0^{k0-1} 2 1
        cn_021 = (
            (odd_idx,) * (sig[odd_idx] - 1)
            + (even_idx,) * (sig[even_idx])
            + (2, odd_idx)
        )
        # 1^{k1-1} 0^{k0-1} 2 0 1 and 1^{k1-2} 01 0^{k0-2} 2 0 1
        cn_201 = swapPair(cn_021, -3)
        swapidx = sig[odd_idx] - 2
    print(
        f"Gluing cross edge stutter {cn_021}-{swapPair(cn_021, swapidx)} and {cn_201}-{swapPair(cn_201, swapidx)}"
    )
    c_12_21_11_01 = glue(
        incorporated_even_even,
        c_01_11,
        (cn_021, swapPair(cn_021, swapidx)),
        (cn_201, swapPair(cn_201, swapidx)),
    )
    # combine the odd_odd_p2 path and the odd_odd_1 cycle
    odd_odd_cycle_02_0 = waveTopRowOddOddOne(odd_odd_1, odd_odd_p2)

    # 1 2 0^{k0-1} 1^{k1-2} 0 1 and 1 0 2 0^{k0-2} 1^{k1-2} 0 1
    # 1 2 0^{k0-1} 1^{k1-1} 0 and 1 0 2 0^{k0-2} 1^{k1-1} 0
    cutnode_even_odds = (
        (odd_idx, 2)
        + (even_idx,) * (sig[even_idx] - 1)
        + (odd_idx,) * (sig[odd_idx] - 2)
        + (even_idx, odd_idx)
    )
    cutnode_odd_odd = swapPair(cutnode_even_odds, -2)
    c_12_21_11_01_02_0 = glue(
        c_12_21_11_01,
        odd_odd_cycle_02_0,
        (cutnode_even_odds, swapPair(cutnode_even_odds, 1)),
        (cutnode_odd_odd, swapPair(cutnode_odd_odd, 1)),
    )
    return c_12_21_11_01_02_0


@cache
def even_1_1_1_cycle(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generates a cycle for the even-1-1-1 case. This is a cycle that contains three paths that are glued to one Hamiltonian cycle in two parts.
    First two nodes are removed from each path to be added to the Hamiltonian cycle. The Hamiltonian cycle is then glued to the rest of the paths (which is a cycle).

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must be of structure even-1-1-1.

    Returns:
        list[tuple[int, ...]]: The Hamiltonian cycle for the even-1-1-1 case.
    """
    # in the odd-1-1-1 we must watch out we don't pick the cross edge xy 0^{k0-1} z 0 ~ yx 0^{k0-1} z 0
    # we use that edge to transform the paths to cycles in this case
    cycle_cover = extend(get_connected_cycle_cover((sig[0] - 1, 1, 1, 1)), (0,))
    # print(f"cycle cover {cycle_cover}")
    # get the even-1-1 path
    even11_path = Hpath_even_1_1(sig[0])
    # transform to other colors
    p1 = extend(transform(even11_path, [0, 3, 2, 1]), (1,))
    p2 = extend(transform(even11_path, [0, 1, 3, 2]), (2,))
    p3 = extend(even11_path, (3,))
    # cut off all the first two elements of these paths to get cycles
    p1_start, p1 = p1[-2:], p1[:-2]
    p2_start, p2 = p2[-2:], p2[:-2]
    p3_start, p3 = p3[-2:], p3[:-2]
    print(f"starts {p1_start} {p2_start} {p3_start}")
    # place the p2 start in the cycle
    cc_p1 = cutCycle(cycle_cover, swapPair(p1_start[0], -2))
    if not adjacent(cc_p1[1], p1_start[1]):
        cc_p1 = cc_p1[:1] + cc_p1[1:][::-1]
    cc_p1 = cc_p1[:1] + p1_start + cc_p1[1:]
    assert pathQ(cc_p1)

    cc_p2 = cutCycle(cc_p1, swapPair(p2_start[0], -2))
    if not adjacent(cc_p2[1], p2_start[1]):
        cc_p2 = cc_p2[:1] + cc_p2[1:][::-1]
    cc_p2 = cc_p2[:1] + p2_start + cc_p2[1:]
    assert pathQ(cc_p2)

    # place the p3 start in the cycle
    cc_p3 = cutCycle(cc_p2, swapPair(p3_start[0], -2))
    if not adjacent(cc_p3[1], p3_start[1]):
        cc_p3 = cc_p3[:1] + cc_p3[1:][::-1]
    cc_p3 = cc_p3[:1] + p3_start + cc_p3[1:]
    assert pathQ(cc_p3)

    print(f"cc_p3; cycleQ {cycleQ(cc_p3)}")
    cut_node_c1 = (2, 3) + (0,) * (sig[0] - 1) + (1, 0)
    cut_node_c1_2 = swapPair(cut_node_c1, -2)
    print(f"cut nodes {cut_node_c1} and {swapPair(cut_node_c1, 1)}")
    cc_c1 = glue(
        cc_p3,
        p1,
        (cut_node_c1, swapPair(cut_node_c1, 1)),
        (cut_node_c1_2, swapPair(cut_node_c1_2, 1)),
    )
    cut_node_c2 = (0,) * sig[0] + (3, 2, 1)
    cut_node_c2_2 = swapPair(cut_node_c2, -2)
    print(f"cut nodes {cut_node_c2} and {swapPair(cut_node_c2, sig[0] - 1)}")
    cc_c2 = glue(
        cc_c1,
        p2,
        (cut_node_c2, swapPair(cut_node_c2, sig[0] - 1)),
        (cut_node_c2_2, swapPair(cut_node_c2_2, sig[0] - 1)),
    )
    cut_node_c3 = (0,) * sig[0] + (1, 3, 2)
    cut_node_c3_2 = swapPair(cut_node_c3, -2)
    print(f"cut nodes {cut_node_c3} and {swapPair(cut_node_c3, sig[0] - 1)}")
    cc_c3 = glue(
        cc_c2,
        p3,
        (cut_node_c3, swapPair(cut_node_c3, sig[0] - 1)),
        (cut_node_c3_2, swapPair(cut_node_c3_2, sig[0] - 1)),
    )
    return [cc_c3]


@cache
def even_2_1_1_cycle(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generates a Hamiltonian cycle for the (even, 2, 1, 1) signature. This is a cycle has two subgraphs that only have a Hamiltonian path.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must be of structure (even, 2, 1, 1).

    Returns:
        list[tuple[int, ...]]: The Hamiltonian cycle for the (even, 2, 1, 1) signature.
    """
    # See master thesis for explanation
    # this list will hold the two subsigs with only one even element
    odd_2_1_1_c0 = extend(get_connected_cycle_cover((sig[0] - 1, 2, 1, 1)), (0,))
    even_1_1_1_c1 = extend(get_connected_cycle_cover((sig[0], 1, 1, 1)), (1,))

    # now the hard part; even-2-1 and even-2-0-1
    even_2_cycles = HpathNS(sig[0], 2)
    even_2_c23_c32 = incorporateSpursInZigZag(
        createZigZagPath(even_2_cycles, (2, 3), (3, 2)),
        stutterPermutations((sig[0], 2)),
        [(3, 2), (2, 3)],
    )
    odd_2_1_c03 = extend(get_connected_cycle_cover((sig[0] - 1, 2, 1)), (0, 3))
    odd_2_0_1_c02 = transform(odd_2_1_c03, [0, 1, 3, 2])
    if sig[0] == 2:
        # the 2-2-1-1 case
        odd_2_1_c03_start, odd_2_1_c03 = odd_2_1_c03[:2], odd_2_1_c03[2:]
        odd_2_0_1_c02_start, odd_2_0_1_c02 = odd_2_0_1_c02[:2], odd_2_0_1_c02[2:]
        print(f"starts 2-2-1-1 {odd_2_1_c03_start} and {odd_2_0_1_c02_start}")
        print(
            f"glued between {(swapPair(odd_2_1_c03_start[0], -2), swapPair(odd_2_1_c03_start[1], -2))} and {(swapPair(odd_2_0_1_c02_start[0], -2), swapPair(odd_2_0_1_c02_start[1], -2))}"
        )
        # now add the start nodes to the c0 cycle
        odd_2_1_1_c0 = glue(
            odd_2_1_1_c0,
            odd_2_1_c03_start,
            (
                swapPair(odd_2_1_c03_start[0], -2),
                swapPair(odd_2_1_c03_start[1], -2),
            ),
            (odd_2_1_c03_start[0], odd_2_1_c03_start[1]),
        )
        odd_2_1_1_c0 = glue(
            odd_2_1_1_c0,
            odd_2_0_1_c02_start,
            (
                swapPair(odd_2_0_1_c02_start[0], -2),
                swapPair(odd_2_0_1_c02_start[1], -2),
            ),
            (odd_2_0_1_c02_start[0], odd_2_0_1_c02_start[1]),
        )
    even_1_1_p12 = extend(
        transform(lemma2_extended_path((2,) * sig[0]), [3, 1, 0]), (1, 2)
    )
    even_1_1_p13 = transform(even_1_1_p12, [0, 1, 3, 2])
    # now remove the first two elements from the even_1_1_p12 and even_1_1_p13 paths
    even_1_1_start12, even_1_1_c12 = even_1_1_p12[:2], even_1_1_p12[2:]
    even_1_1_start13, even_1_1_c13 = even_1_1_p13[:2], even_1_1_p13[2:]
    print(f"Even-2-1-1 case starts with {even_1_1_start12} and {even_1_1_start13}")
    # now add the start nodes to the c1 cycle
    even_1_1_1_c1 = glue(
        even_1_1_1_c1,
        even_1_1_start12,
        (swapPair(even_1_1_start12[0], -2), swapPair(even_1_1_start12[1], -2)),
        (even_1_1_start12[0], even_1_1_start12[1]),
    )
    even_1_1_1_c1 = glue(
        even_1_1_1_c1,
        even_1_1_start13,
        (swapPair(even_1_1_start13[0], -2), swapPair(even_1_1_start13[1], -2)),
        (even_1_1_start13[0], even_1_1_start13[1]),
    )
    # combine c2 and c3 to get order; c0, c1, c2/c3
    cn103 = (1, 0, 2) + (0,) * (sig[0] - 2) + (1, 0, 3)
    cn013 = swapPair(cn103, -3)
    swap103_013 = 0
    c03_13 = glue(
        odd_2_1_c03,
        even_1_1_c13,
        (cn103, swapPair(cn103, swap103_013)),
        (cn013, swapPair(cn013, swap103_013)),
    )
    cn102 = (1, 0, 3) + (0,) * (sig[0] - 2) + (1, 0, 2)
    cn012 = swapPair(cn102, -3)
    swap102_012 = 0
    c02_12 = glue(
        odd_2_0_1_c02,
        even_1_1_c12,
        (cn102, swapPair(cn102, swap102_012)),
        (cn012, swapPair(cn012, swap102_012)),
    )
    cn213 = (0,) * (sig[0]) + (1, 2, 1, 3)
    cn123 = swapPair(cn213, -3)
    swap213_123 = sig[0] - 1
    c02_12_23_32 = glue(
        c03_13,
        even_2_c23_c32,
        (cn213, swapPair(cn213, swap213_123)),
        (cn123, swapPair(cn123, swap213_123)),
    )
    cn312 = (0,) * (sig[0]) + (1, 3, 1, 2)
    cn132 = swapPair(cn312, -3)
    swap213_123 = sig[0] - 1
    c2_c3 = glue(
        c02_12,
        c02_12_23_32,
        (cn312, swapPair(cn312, swap213_123)),
        (cn132, swapPair(cn132, swap213_123)),
    )

    cn30 = (0,) * (sig[0] - 1) + (1, 1, 2, 3, 0)
    cn03 = swapPair(cn30, -2)
    swap30_03 = sig[0]
    c0_c2_c3 = glue(
        odd_2_1_1_c0,
        c2_c3,
        (cn30, swapPair(cn30, swap30_03)),
        (cn03, swapPair(cn03, swap30_03)),
    )
    cn31 = (0,) * (sig[0]) + (1, 2, 3, 1)
    cn13 = swapPair(cn31, -2)
    swap31_13 = sig[0]
    cycle = glue(
        even_1_1_1_c1,
        c0_c2_c3,
        (cn31, swapPair(cn31, swap31_13)),
        (cn13, swapPair(cn13, swap31_13)),
    )
    return [cycle]


@cache
def two_odd_rest_even_cycle_cover(
    sig: tuple[int, ...]
) -> tuple[list[list[tuple[int, ...]]], list[list[tuple[int, ...]]]]:
    """
    Generates the disjoint cycle cover on the permutations for the given signature `sig`.
    This handles the case where there are two odd elements and the rest are even.
    This is done by fixing the trailing element or trailing two elements if the trailing element is odd to incorporate stutter permutations.
    For more explanation, see the master thesis.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must have at least one element.

    Returns:
        tuple[list[list[tuple[int, ...]]], list[list[tuple[int, ...]]]: The disjoint cycle cover for the given signature `sig`.
        The first list contains the disjoint cycle cover for the permutations where the last element is even.
        The second list contains the disjoint cycle cover for the permutations where the last element is odd.
    """
    # This is the case where there were stutters in the previous signatures but now there are none
    all_sub_cycles = []
    # this list will hold the two subsigs with only one odd element
    two_odd_subsig_added = False
    last_odd_cycle = []
    for idx, color in enumerate(sig):
        sub_sig = sig[:idx] + (color - 1,) + sig[idx + 1 :]
        current_subcycle = []
        if sum(n % 2 for n in sub_sig) == 1:
            tails = []
            # get the index of the odd element
            odd_idx = next(i for i, v in enumerate(sub_sig) if v % 2 == 1)
            # add the _odd-odd part
            even_subsig = (
                sub_sig[:odd_idx] + (sub_sig[odd_idx] - 1,) + sub_sig[odd_idx + 1 :]
            )
            even_indices = [i for i, v in enumerate(sig) if v % 2 == 0]
            if sub_sig[idx] > 1:
                sub_sub_sig_extra = (
                    sub_sig[:idx] + (sub_sig[idx] - 1,) + sub_sig[idx + 1 :]
                )
                current_subcycle.append(
                    [
                        extend(
                            get_connected_cycle_cover(sub_sub_sig_extra),
                            (idx,),
                        )
                    ]
                )
                tails.append((idx,))
            for i in even_indices:
                two_odd_subsubsig = sub_sig[:i] + (sub_sig[i] - 1,) + sub_sig[i + 1 :]
                sorted_subsub_sig, tran = get_transformer(
                    two_odd_subsubsig, lambda x: [x[0] % 2 == 1, x[0]]
                )
                print(
                    f"\033[1m\033[91mSUBSUUBSIG {two_odd_subsubsig} sorted {sorted_subsub_sig} tran {tran}\033[0m\033[0m"
                )
                if len(list(two_odd_subsubsig)) == 3 and two_odd_subsubsig == (2, 3, 1):
                    current_subcycle.append(
                        [
                            extend(
                                transform(
                                    incorporated_odd_2_1_cycle(
                                        sorted_subsub_sig[0], True
                                    ),
                                    [1, 0, 2],
                                ),
                                (i,),
                            ),
                        ]
                    )
                elif (
                    len(sorted_subsub_sig) == 3
                    and two_odd_subsubsig[2] == 1
                    and (
                        (
                            two_odd_subsubsig[0] % 2 == 0
                            and two_odd_subsubsig[0] - two_odd_subsubsig[1] < 1
                            and two_odd_subsubsig[0] > two_odd_subsubsig[1]
                        )
                        or (
                            two_odd_subsubsig[1] % 2 == 0
                            and two_odd_subsubsig[1] > 2
                            and two_odd_subsubsig[1] - two_odd_subsubsig[0] < 1
                        )
                    )
                ):
                    current_subcycle.append(
                        [
                            extend(
                                transform(
                                    even_odd_1_cycle(
                                        (sorted_subsub_sig[0], sorted_subsub_sig[2], 1),
                                        False,
                                    ),
                                    [tran[0], tran[2], tran[1]],
                                ),
                                (i,),
                            )
                        ]
                    )
                    print(f"even-odd-1 cycle Distinct ends {False}")
                else:
                    current_subcycle.append(
                        [
                            extend(
                                get_connected_cycle_cover(two_odd_subsubsig),
                                (i,),
                            ),
                        ]
                    )
                tails.append((i,))
            prepended_tails = []
            for i, tail in enumerate(tails[:-1]):
                prepended_tails.append((tails[(i + 1) % len(tails)][0],) + tail)
            if len(current_subcycle) > 1:
                connected_current = connect_single_cycle_cover(
                    current_subcycle, prepended_tails
                )
            else:
                connected_current = current_subcycle[0][0]
            last_odd_cycle.append([extend(connected_current, (idx,))])
            if not two_odd_subsig_added:
                two_odd_subsig_added = True
                cycle_without_stutters = get_connected_cycle_cover(even_subsig)
                odds_non_stutter_cycle = createZigZagPath(
                    cycle_without_stutters, (idx, odd_idx), (odd_idx, idx)
                )
                tails.append((odd_idx, idx))
                odds_stutter_permutations = stutterPermutations(even_subsig)
                cycle_with_stutters = incorporateSpursInZigZag(
                    odds_non_stutter_cycle,
                    odds_stutter_permutations,
                    [(odd_idx, idx), (idx, odd_idx)],
                )
                last_odd_cycle.append([cycle_with_stutters])
        else:
            c = get_connected_cycle_cover(sub_sig)
            all_sub_cycles.append([extend(c, (idx,))])
    return all_sub_cycles, last_odd_cycle


@cache
def two_odd_rest_even_cycle(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generates a Hamiltonian cycle for the given signature `sig` where there are two odd elements and the rest are even.
    This uses the disjoint cycle cover generated by the `two_odd_rest_even_cycle_cover` function to generate the Hamiltonian cycle.
    The individual cycles are connected by cross edges to form the Hamiltonian cycle.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must have two odd occurring colors.

    Returns:
        list[tuple[int, ...]]: The Hamiltonian cycle for the given signature `sig`.
    """
    all_sub_cycles, last_odd_cycle = two_odd_rest_even_cycle_cover(sig)
    odd_idx1, odd_idx2 = [i for i, v in enumerate(sig) if v % 2 == 1]
    last_even_idx = next(i for i, v in enumerate(sig) if v % 2 == 0)
    last_even_idx = [i for i, v in enumerate(sig) if v % 2 == 0][-1]
    # the connecting tails are 201, 021 for signature (3, 3, 2)
    # since we cannot guarantee that there are more odd colors, we use an even color to swap to the tail
    temp = [
        (odd_idx2, last_even_idx, odd_idx1),
        (last_even_idx, odd_idx1, odd_idx2),
    ]
    # first odd indices then the even indices;
    t1 = (odd_idx2, last_even_idx, odd_idx1)
    t2 = (odd_idx1, last_even_idx, odd_idx2)
    tail1_sig = list(get_perm_signature(t1)) + [0] * (
        len(list(sig)) - len(get_perm_signature(t1))
    )
    tail2_sig = list(get_perm_signature(t2)) + [0] * (
        len(list(sig)) - len(get_perm_signature(t2))
    )
    lambda_func = lambda x: x[1]
    all_elements1 = sorted(
        [[i, n - (i in t1)] for i, n in enumerate(sig)],
        key=lambda_func,
        reverse=True,
    )
    all_elements2 = sorted(
        [[i, n - (i in t2)] for i, n in enumerate(sig)],
        key=lambda_func,
        reverse=True,
    )
    odd_elements1 = [[i, n] for i, n in all_elements1 if n % 2 == 1]
    even_elements1 = [[i, n] for i, n in all_elements1 if n % 2 == 0]
    odd_elements2 = [[i, n] for i, n in all_elements2 if n % 2 == 1]
    even_elements2 = [[i, n] for i, n in all_elements2 if n % 2 == 0]
    # node1 is a tuple of; the odd elements then the even elements in pairs of 2
    print(
        f"odd elements {odd_elements1} - {odd_elements2} and even elements {even_elements1} - {even_elements2}"
    )
    node1 = tuple()
    for even_el, even_occ in even_elements1:
        node1 += tuple([even_el] * even_occ)
    for odd_el, odd_occ in odd_elements1:
        node1 += tuple([odd_el] * odd_occ)
    node1_first = node1 + temp[0]
    node1_second = node1 + swapPair(temp[0], 0)
    swapindex1 = sum([n[1] for n in even_elements2]) - 1
    node2 = tuple()
    for even_el, even_occ in even_elements2:
        node2 += tuple([even_el] * even_occ)
    for odd_el, odd_occ in odd_elements2:
        node2 += tuple([odd_el] * odd_occ)
    node2_first = node2 + temp[1]
    node2_second = node2 + swapPair(temp[1], 0)
    swapindex2 = swapindex1
    # find_cross_edges(last_odd_cycle[:2], temp[:1])
    print(f"sig {sig} last odd cycle")
    print(
        f"\033[1m\033[92mChosen cross edges {temp[0], swapPair(temp[0], 0)} and {temp[1], swapPair(temp[1], 0)}:\n {((node1_first, swapPair(node1_first, swapindex1)), (node1_second, swapPair(node1_second, swapindex1)))} and {((node2_first, swapPair(node2_first, swapindex2)), (node2_second, swapPair(node2_second, swapindex2)))}\033[0m\033[0m"
    )

    connected_odds1 = glue(
        last_odd_cycle[0][0],
        last_odd_cycle[1][0],
        (node1_first, swapPair(node1_first, swapindex1)),
        (node1_second, swapPair(node1_second, swapindex1)),
    )
    connected_odds2 = glue(
        connected_odds1,
        last_odd_cycle[2][0],
        (node2_first, swapPair(node2_first, swapindex2)),
        (node2_second, swapPair(node2_second, swapindex2)),
    )
    print(f"connected odds 2 is a cycle {cycleQ(connected_odds2)}")
    all_sub_cycles.append([connected_odds2])
    return all_sub_cycles


@cache
def generate_cycle_cover(sig: tuple[int, ...]) -> list[list[tuple[int, ...]]]:
    """
    Generates the disjoint cycle cover on the non-stutter permutations for the given signature `sig` according to the Theorem by Verhoeff.\n
    **Theorem:** *When the arity is at least 3 and at most one k i is odd, the neighbor-swap graph
    of non-stutter permutations admits a disjoint cycle cover, that is, a set of vertex-disjoint
    cycles that visit all permutations exactly once.*\n
    This is split into several cases below. Note that Even-1-1 and Odd-1-1 form a cycle together:\n
    - Arity 1: The cycle is a single node of 0's.
    - Arity 2: The cycle is a single cycle of 0's and 1's. Using Verhoeff's binary theorem.
    - Even-1-1: A **path** from `c = 1 2 0^k0` to `d = 0 2 1 0^(k0-1)`. Does not contain a cycle.
    - Odd-1-1: The cycle from `1 0^k0 2` to `0 1 0^(k0-1) 2`.
    - Odd-2-1: A **path** from `a = 1 2 0^{k0} 1` to `b = 0 2 1 0^{k0-1} 1`. (Also contains a cycle by Stachowiak's theorem)
    - Even-2-1: A cycle formed by the path from Even-1-1 and Odd-2-1.
    - All-but-one-even: Forms cycles by fixing the trailing element. (uses Stachowiak's Lemma 11 for the two-or-more-odd case)
    - All-even: Forms cycles by fixing the trailing *two* elements.
    - Two-or-more-odd: Stachowiak's theorem gives us a cycle on this graph.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must have at least one element.

    Returns:
        list[list[tuple[int, ...]]]:
            The cycle cover for the given signature `sig`.\n
            Every list of tuples is a cycle in the cycle cover. The tuples are permutations.
            The lists do not have a defined depth since they can consist of cycle covers themselves. But the depth is at least 2.

    Raises:
        ValueError: If the signature is empty.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
    """
    # sort list in descending order
    if len(list(sig)) == 0:
        return []
    elif any(n < 0 for n in sig):
        raise ValueError("Signature cannot contain negative numbers")
    elif len(list(sig)) == 1:
        return [[(0,) * sig[0]]]
    sorted_sig, transformer = get_transformer(sig, lambda x: x[0])
    if sorted_sig != sig:
        if sig == (1, 2, 1):
            return [Hpath_odd_2_1(1)]
        return transform_cycle_cover(generate_cycle_cover(sorted_sig), transformer)
    k = sig[0]
    if len(list(sig)) == 2:
        return [HpathNS(sig[0], sig[1])]
    elif 0 in sig:
        return generate_cycle_cover(sig[:-1])
    # Odd-1-1
    elif len(list(sig)) == 3 and k % 2 == 1 and sig[1] == 1 and sig[2] == 1:
        # A cycle from 1 0^k 2 to 0 1 0^(k-1) 2
        lemma2_stachowiak = lemma2_extended_path(tuple([2] * k), False)
        transformed_lemma2 = cutCycle(
            transform(lemma2_stachowiak, [2, 1, 0]), (1,) + tuple([0] * k) + (2,)
        )
        return [transformed_lemma2]
    # Even-1-1
    elif len(list(sig)) == 3 and k % 2 == 0 and sig[1] == 1 and sig[2] == 1:
        # The path from 1 2 0^k to 0 2 1 0^(k-1)
        return [Hpath_even_1_1(k)]
    # even-2-1 case
    elif len(list(sig)) == 3 and k % 2 == 0 and sig[1] == 2 and sig[2] == 1:
        return even_2_1_cycle(k)
    # odd-2-1 case
    elif len(list(sig)) == 3 and k % 2 == 1 and sig[1] == 2 and sig[2] == 1:
        # a cycle from 1 0^k 1 2 to 1 0^(k-1) 1 0 2
        return [incorporated_odd_2_1_cycle(k)]
    # even-odd-1 case
    elif (
        len(list(sig)) == 3
        and ((k % 2 == 1 and sig[1] % 2 == 0) or (k % 2 == 0 and sig[1] % 2 == 1))
        and sig[2] == 1
    ):
        return [even_odd_1_cycle(sig)]
    # odd-odd-1 case
    elif len(list(sig)) == 3 and k % 2 == 1 and sig[1] % 2 == 1 and sig[2] == 1:
        return odd_odd_1_cycle(sig)
    # even-2-1-1 case
    elif (
        len(list(sig)) == 4
        and k % 2 == 0
        and sig[1] == 2
        and sig[2] == 1
        and sig[3] == 1
    ):
        return even_2_1_1_cycle(sig)
    # two-odds, rest even case (odd-odd-rest-even)
    elif sum(n % 2 for n in sig) == 2:
        return two_odd_rest_even_cycle(sig)
    # if there are three 1's and only one even number; even-1-1-1 case
    elif len(sig) == 4 and sig[0] % 2 == 0 and all(n == 1 for n in sig[1:]):
        return even_1_1_1_cycle(sig)
    # three-or-more-odd case
    elif sum(n % 2 for n in sig) >= 3:
        # use induction on the last element
        all_sub_cycles = []
        # sort the signature to first have the even numbers then the odd numbers
        sorted_sig, transformer = get_transformer(sig, lambda x: [x[0]])
        print(f"new sig {sorted_sig} and transformer {transformer}")
        for idx, color in enumerate(sorted_sig):
            sub_sig = sorted_sig[:idx] + (color - 1,) + sorted_sig[idx + 1 :]
            if any(s < 0 for s in sub_sig):
                raise ValueError(f"Negative signature {sub_sig}")
            else:
                c = get_connected_cycle_cover(sub_sig)
            if not isinstance(c[0], tuple):
                raise ValueError(f"Expected a cycle, got {c}")
            all_sub_cycles.append([extend(c, (idx,))])
        # connect the cycles
        single_cycle = connect_single_cycle_cover(
            all_sub_cycles, generate_end_tuple_order(sig)
        )
        # transform the cycle back to the original order
        return [transform(single_cycle, transformer)]
    # all-but-one even case
    elif sum(n % 2 for n in sig) == 1:
        all_sub_cycles = []
        for idx, color in enumerate(sig):
            sub_sig = sig[:idx] + (color - 1,) + sig[idx + 1 :]
            c = generate_cycle_cover(sub_sig)
            all_sub_cycles.append(extend_cycle_cover(c, (idx,)))
        return all_sub_cycles
    # all-even case
    else:
        all_sub_cycles = generate_all_even_cycle_cover(sig)
        return all_sub_cycles


def connect_cycles_recursive(
    cycle_cover: list[list], sig: tuple[int, ...]
) -> list[list[tuple[int, ...]]]:
    """
    Connects cycles in a cycle cover recursively. This is equal to the inductive step of our proof.

    Args:
        cycle_cover (list[list]): The cycle cover to connect. This list has an unknown depth
        sig (tuple[int, ...]): The signature of the permutations. Must have at least

    Returns:
        list[list[tuple[int, ...]]]: The connected cycle cover as a list of tuples, where each tuple represents a permutation.
    """
    tail_length = get_tail_length(sig)
    single_cycle_cover = []
    for nested_cycle in cycle_cover:
        if (
            isinstance(nested_cycle, list)
            and isinstance(nested_cycle[0], list)
            and isinstance(nested_cycle[0][0], list)
        ):
            # we need to remove tails from every list in the nested cycle to connect them
            first_cycle_element = get_first_element(nested_cycle)

            # Get the new signature
            subsig = get_perm_signature(first_cycle_element[:-tail_length])
            sorted_subsig, subsig_transformer = get_transformer(subsig, lambda x: x[0])
            if sum(n % 2 for n in sig) == 2 and sum(n % 2 for n in subsig) == 1:
                print(
                    f"TEST subsiggg {subsig} {sorted_subsig} last element {first_cycle_element} {sum(n % 2 for n in subsig)}"
                )

                # now we should incorporate the stutters in the cycle
            # TODO check if we have to incorporate stutters (when two colors are odd)
            connected_shortened = get_connected_cycle_cover(sorted_subsig)
            # Now we need to add the last element back to the connected shortened cycle
            if isinstance(connected_shortened[0], tuple):
                connected_shortened = [connected_shortened]
            # now transform the connected shortened subsig back to the original values
            transformed_short = transform_cycle_cover(
                connected_shortened, subsig_transformer
            )
            connected = extend_cycle_cover(
                transformed_short, first_cycle_element[-tail_length:]
            )
            single_cycle_cover.append(connected)
        else:
            single_cycle_cover.append(nested_cycle)
    return single_cycle_cover


@cache
def get_connected_cycle_cover(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Computes the a cycle on the non-stutter permutations for a given signature.
    If the signature is odd-2-1, the connected cycle cover is computed using lemma 11 by Stachowiak.
    Otherwise Verhoeff's cycle cover theorem is used to generate the cycle cover and that is then connected using the ``connect_cycle_cover`` function.

    Args:
        sig (tuple[int, ...]): The signature for which the cycle on non-stutter permutations needs to be computed.

    Returns:
        list[tuple[int, ...]]: The connected cycle cover as a list of tuples, where each tuple represents a permutation.

    Raises:
        AssertionError: If the generated cycle cover by Verhoeff's theorem is empty.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
    """
    sorted_sig, transformer = get_transformer(sig, lambda x: x[0])
    if len(list(sig)) <= 1:
        # if there is one element, it is a stutter permutation by definition
        return []
    if sig != sorted_sig:
        return transform(get_connected_cycle_cover(sorted_sig), transformer)
    elif len(list(sig)) == 2 and any(c % 2 == 0 for c in sig):
        return HpathNS(sig[0], sig[1])
    # this is just binary to get the path/cycle of Verhoeff
    elif len(list(sig)) < 3:
        return HpathNS(sig[0], sig[1])
    else:
        cover = generate_cycle_cover(sig)
        assert len(cover) > 0
        if len(cover) == 1:
            return cover[0]
        elif isinstance(cover[0][0], int):
            return cover
        # If there is less than two odd occurring colors, we can connect the cycles using the recursive connection method
        # Loop over the cycles in the cover and connect the cycle at index `i` ends with an element of color `i`
        # while the depth of the list is more than 2, we need to connect the previous cycles
        single_cycle_cover = connect_cycles_recursive(cover, sig)
        connected_cover = connect_single_cycle_cover(
            single_cycle_cover, generate_end_tuple_order(sig)
        )
        return connected_cover


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a cycle cover from a given permutation signature."
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
    s = tuple([int(x) for x in args.signature.split(",")])
    if len(list(s)) > 1:
        perms = generate_cycle_cover(s)
        if args.verbose:
            print(f"Resulting path {perms}")
        for p in perms:
            first = get_first_element(p)
            print(f"last number: {first[-2:]}")
        stut_count = len(stutterPermutations(s))
        try:
            total_perms = recursive_cycle_check(perms)
            print(
                f"Verhoeff's result for signature {s}: {total_perms}/{multinomial(s)} "
                f"(incl {stut_count} stutters {stut_count+total_perms}) is a list of cycles."
            )
            non_stutters = nonStutterPermutations(s)
        except AssertionError as e:
            print(f"List of cycles is not a valid cycle cover: {e}")
            print(
                f"Path: {pathQ(perms[0])}, Cycle: {cycleQ(perms[0])}. The expected length is {multinomial(s)}"
            )
