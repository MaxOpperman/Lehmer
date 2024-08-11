import argparse
import collections

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
    createZigZagPath,
    cutCycle,
    cycleQ,
    get_first_element,
    get_transformer,
    glue,
    incorporateSpurInZigZag,
    incorporateSpursInZigZag,
    pathQ,
    recursive_cycle_check,
    shorten_cycle_cover,
    splitPathIn2,
    transform,
    transform_cycle_cover,
)
from helper_operations.permutation_graphs import (
    extend,
    extend_cycle_cover,
    get_perm_signature,
    multinomial,
    rotate,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma2_extended_path, lemma11
from steinhaus_johnson_trotter import SteinhausJohnsonTrotter
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
                sorted_sub_sig[0] % 2 == 0
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
                # this gives two parallel paths which we need to combine into a cycle
                sub_cycles = []
                print(f"cycle cover {cycle_cover}")
                if len(cycle_cover) == 1:
                    sub_cycles.append(
                        extend(cycle_cover[0], (idx2, idx))[::-1]
                        + extend(cycle_cover[0], (idx, idx2))
                    )
                else:
                    for cyc in cycle_cover:
                        if len(cyc) > 1:
                            print(f"cycle {cyc}")
                            quit()
                        sub_cycles.append(
                            extend(cyc[0], (idx2, idx))[::-1]
                            + extend(cyc[0], (idx, idx2))
                        )
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
    # all-1's case
    elif all(n == 1 for n in sig):
        # use the Steinhaus-Johnson-Trotter algorithm to generate the cycle
        sjt = SteinhausJohnsonTrotter()
        return [sjt.get_sjt_permutations(len(sig))]
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
        even_odd_1 = extend_cycle_cover(
            generate_cycle_cover((sig[0] - 1, sig[1] - 1, 1)), (even_idx, odd_idx)
        )

        # odd-2, even, 1 (appended with odd, odd); so odd, even, 1 (but a smaller case)
        odd_even_1 = extend_cycle_cover(
            generate_cycle_cover(
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
        even_even_c2odd_odd2 = createZigZagPath(
            HpathNS(sig[0] - (sig[0] % 2), sig[1] - (sig[1] % 2)),
            (2, odd_idx),
            (odd_idx, 2),
        )
        even_even_stutter_perms = stutterPermutations(
            (sig[0] - (sig[0] % 2), sig[1] - (sig[1] % 2))
        )
        # odd-1, even (appended with odd, 2 and 2, odd) and stutters incorporated; so even, even
        incorporated_even_even = incorporateSpursInZigZag(
            even_even_c2odd_odd2,
            even_even_stutter_perms,
            [(odd_idx, 2), (2, odd_idx)],
        )

        if sig[odd_idx] - 2 == 1:
            odd_even_1_tip, odd_even_1 = odd_even_1[0][-2:], [odd_even_1[0][:-2]]
            even_odd_cut = cutCycle(even_odd_1[0], swapPair(odd_even_1_tip[0], -3))
            if even_odd_cut[1] != swapPair(odd_even_1_tip[1], -3):
                even_odd_cut = even_odd_cut[:1] + even_odd_cut[1:][::-1]
            even_odd_1 = [even_odd_cut[:1] + odd_even_1_tip + even_odd_cut[1:]]

        # assume odd is 0 and even is 1
        # 0 2 1^{k1-1} 0^{k0-2} 1 0 and 0 2 1^{k1-1} 0^{k0-3} 1 00
        cutnode_even_odd = (
            (odd_idx, 2)
            + (even_idx,) * (sig[even_idx] - 1)
            + (odd_idx,) * (sig[odd_idx] - 2)
            + (even_idx, odd_idx)
        )
        cutnode_odd_even = swapPair(cutnode_even_odd, -3)
        even_odds_combined = glue(
            even_odd_1[0],
            odd_even_1[0],
            (cutnode_even_odd, swapPair(cutnode_even_odd, 1)),
            (cutnode_odd_even, swapPair(cutnode_odd_even, 1)),
        )

        # combine the odd_odd_p2 path and the odd_odd_1 cycle
        odd_odd_cycle = waveTopRowOddOddOne(odd_odd_1, odd_odd_p2)

        # 2 0 1^{k1-1} 0^{k0-2} 1 0 and 2 0 1^{k1-1} 0^{k0-1} 1
        cutnode_even_odds = swapPair(cutnode_even_odd, 0)
        cutnode_odd_odd = swapPair(cutnode_even_odds, -2)
        odd_odd_combined = glue(
            even_odds_combined,
            odd_odd_cycle,
            (cutnode_even_odds, swapPair(cutnode_even_odds, 1)),
            (cutnode_odd_odd, swapPair(cutnode_odd_odd, 1)),
        )

        # 0^{k0-1} 1^{k1} 2 0 and 0 ^{k0-2} 1 0 1^{k1-1} 2 0
        cut_node1 = (
            (odd_idx,) * (sig[odd_idx] - 1)
            + (even_idx,) * (sig[even_idx])
            + (2, odd_idx)
        )
        cut_node2 = swapPair(cut_node1, sig[odd_idx] - 2)
        last_combined = glue(
            odd_odd_combined,
            incorporated_even_even,
            (swapPair(cut_node1, -3), swapPair(cut_node2, -3)),
            (cut_node1, cut_node2),
        )
        print(f"last combined {last_combined} {cycleQ(last_combined)}")
        print(f"EVEN {even_idx} missing {set(lemma11(sig)) - set(last_combined)}")
        print(
            f"duplicates {[item for item, count in collections.Counter(last_combined).items() if count > 1]}"
        )
        return [last_combined]
    # odd-odd-1 case
    elif len(list(sig)) == 3 and k % 2 == 1 and sig[1] % 2 == 1 and sig[2] == 1:
        # easy first; odd-even-1 and even-odd-1
        even_odd_1 = extend(get_connected_cycle_cover((sig[0] - 1, sig[1], 1)), (0,))
        odd_even_1 = extend(get_connected_cycle_cover((sig[0], sig[1] - 1, 1)), (1,))

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
        odd_odd_xx = extend(HpathNS(sig[0] - 2, sig[1]), (0, 0, 2))
        odd_odd_yy = extend(HpathNS(sig[0], sig[1] - 2), (1, 1, 2))
        even_odd_cut = [waveTopRowOddOddOne(even_odd_1, odd_odd_xx)]
        odd_even_cut = [waveTopRowOddOddOne(odd_even_1, odd_odd_yy)]

        return [even_odd_cut, odd_even_cut, extended_odd_odd]
    # two-odds, rest even case
    elif sum(n % 2 for n in sig) == 2:
        # This is the case where there were stutters in the previous signatures but now there are none
        all_sub_cycles = []
        # this list will hold the two subsigs with only one odd element
        two_odd_subsigs = []
        last_odd_cycle = []
        even_one_one_cycle = []
        even_one_one_done = False
        total_length = 0
        for idx, color in enumerate(sig):
            sub_sig = sig[:idx] + (color - 1,) + sig[idx + 1 :]
            print(f"\033[1m\033[91msubsig {sub_sig} \033[0m\033[0m")
            current_subcycle = []
            # print(f"c {sub_sig}-{get_perm_signature(get_first_element(c))} {c}")
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
                    print(f"subsubsig {sub_sub_sig_extra}")
                    subsubsig_sorted, _ = get_transformer(
                        sub_sub_sig_extra, lambda x: [x[0] % 2, x[0]]
                    )
                    print(
                        f"subsubsig {sub_sub_sig_extra} {subsubsig_sorted} with two subtracted from {idx}"
                    )
                    if (
                        len(list(subsubsig_sorted)) == 3
                        and subsubsig_sorted[0] == 1
                        and subsubsig_sorted[1] == 1
                        and subsubsig_sorted[2] % 2 == 0
                    ):
                        if len(even_one_one_cycle) == 0:
                            even_one_one_cycle.extend(
                                extend(
                                    get_connected_cycle_cover(sub_sub_sig_extra),
                                    (idx, idx),
                                )
                            )
                        else:
                            assert not even_one_one_done
                            even_one_one_cycle.extend(
                                extend(
                                    get_connected_cycle_cover(sub_sub_sig_extra),
                                    (idx, idx),
                                )
                            )
                            print(f"even one one cycle {[even_one_one_cycle]}")
                            current_subcycle.append([even_one_one_cycle])
                            tails.append((idx, idx))
                            even_one_one_done = True
                    else:
                        print(f"{get_connected_cycle_cover(sub_sub_sig_extra)}")
                        current_subcycle.append(
                            [
                                extend(
                                    get_connected_cycle_cover(sub_sub_sig_extra),
                                    (idx, idx),
                                )
                            ]
                        )
                        tails.append((idx, idx))
                for i in even_indices:
                    two_odd_subsubsig = (
                        sub_sig[:i] + (sub_sig[i] - 1,) + sub_sig[i + 1 :]
                    )
                    # one of the tails is even but now it is the first element in the tail
                    sorted_two_odd, _ = get_transformer(
                        two_odd_subsubsig, lambda x: [x[0] % 2, x[0]]
                    )
                    print(f"two odd subsubsig {two_odd_subsubsig} {sorted_two_odd}")
                    # if it is even-1-1, we need to remember the path for later
                    if (
                        len(list(sorted_two_odd)) == 3
                        and sorted_two_odd[0] == 1
                        and sorted_two_odd[1] == 1
                        and sorted_two_odd[2] % 2 == 0
                    ):
                        if len(even_one_one_cycle) == 0:
                            print(f"even one one cycle {two_odd_subsubsig}")
                            even_one_one_cycle.extend(
                                extend(
                                    get_connected_cycle_cover(two_odd_subsubsig),
                                    (i, idx),
                                )
                            )
                        else:
                            assert not even_one_one_done
                            even_one_one_cycle.extend(
                                extend(
                                    get_connected_cycle_cover(two_odd_subsubsig),
                                    (i, idx),
                                )
                            )
                            print(f"even one one cycle {[even_one_one_cycle]}")
                            current_subcycle.append([even_one_one_cycle])
                            tails.append((i, idx))
                            even_one_one_done = True
                    # check if this results an odd-2-1 case, then we need a cycle and not a path
                    elif (
                        len(list(sorted_two_odd)) == 3
                        and sorted_two_odd[0] % 2 == 1
                        and sorted_two_odd[1] == 1
                        and sorted_two_odd[2] == 2
                    ):
                        current_subcycle.append(
                            [extend(lemma11(two_odd_subsubsig), (i, idx))]
                        )
                        print(
                            f"connected {get_connected_cycle_cover(two_odd_subsubsig)}"
                        )
                        tails.append((i, idx))
                    else:
                        print(
                            f"two odd {two_odd_subsubsig} {get_connected_cycle_cover(two_odd_subsubsig)} {i} {idx}"
                        )
                        current_subcycle.append(
                            [
                                extend(
                                    get_connected_cycle_cover(two_odd_subsubsig),
                                    (i, idx),
                                )
                            ]
                        )
                        tails.append((i, idx))
                if even_subsig not in two_odd_subsigs:
                    two_odd_subsigs.append(even_subsig)
                    cycle_without_stutters = get_connected_cycle_cover(even_subsig)
                    odds_non_stutter_cycle = createZigZagPath(
                        cycle_without_stutters, (idx, odd_idx), (odd_idx, idx)
                    )
                    tails.append((odd_idx, idx))
                    odds_stutter_permutations = stutterPermutations(even_subsig)
                    print(
                        f"Odd stutters {even_subsig} {odds_stutter_permutations} between zigzag {odds_non_stutter_cycle[0]} - {odds_non_stutter_cycle[-1]}"
                    )
                    cycle_with_stutters = incorporateSpursInZigZag(
                        odds_non_stutter_cycle,
                        odds_stutter_permutations,
                        [(odd_idx, idx), (idx, odd_idx)],
                    )
                    current_subcycle.append([cycle_with_stutters])
                prepended_tails = []
                for i, tail in enumerate(tails):
                    prepended_tails.append((tails[(i + 1) % len(tails)][0],) + tail)
                print(
                    f"prepended tails {prepended_tails} and current subcycle {current_subcycle}"
                )
                if len(current_subcycle) > 1:
                    connected_current = connect_single_cycle_cover(
                        current_subcycle, prepended_tails
                    )
                else:
                    connected_current = current_subcycle[0][0]

                last_odd_cycle.append([connected_current])
                # add the other parts of the since they are not in the zig-zag path
            else:
                c = get_connected_cycle_cover(sub_sig)
                total_length += len(c)
                all_sub_cycles.append([extend(c, (idx,))])
        odd_idx1, odd_idx2 = [i for i, v in enumerate(sig) if v % 2 == 1]
        first_even_idx = next(i for i, v in enumerate(sig) if v % 2 == 0)
        # the connecting tails are 201, 021 for signature (3, 3, 2)
        # since we cannot guarantee that there are more odd colors, we use an even color to swap to the tail
        print(f"last odd cycle {last_odd_cycle}")
        connected_odds = connect_single_cycle_cover(
            last_odd_cycle,
            [
                (first_even_idx, odd_idx1, odd_idx2),
                (odd_idx1, first_even_idx, odd_idx2),
            ],
        )
        all_sub_cycles.append([connected_odds])
        total_length += len(connected_odds)
        print(f"total length {total_length}")
        return all_sub_cycles
    # three-or-more-odd case
    elif sum(n % 2 for n in sig) >= 3:
        return [lemma11(sig)]
    # all-but-one even case
    elif sum(n % 2 for n in sig) == 1:
        all_sub_cycles = []
        for idx, color in enumerate(sig):
            sub_sig = sig[:idx] + (color - 1,) + sig[idx + 1 :]
            # check if this results an odd-2-1 case, then we need a cycle and not a path
            sorted_sub_sig, transformer2 = get_transformer(
                sub_sig, lambda x: [x[0] % 2, x[0]]
            )
            if (
                sorted_sub_sig[0] % 2 == 1
                and sorted_sub_sig[1] == 1
                and sorted_sub_sig[2] == 2
            ):
                c = [transform(lemma11(sorted_sub_sig), transformer2)]
            else:
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
            print(
                f"OTHER subsiggg {sig} {get_first_element(nested_cycle)} {sum(n % 2 for n in sig)}"
            )
            single_cycle_cover.append(nested_cycle)
    return single_cycle_cover


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
    if len(list(sig)) == 0:
        return []
    sorted_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])
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
        tail_length = get_tail_length(sig)
        # while the depth of the list is more than 2, we need to connect the previous cycles
        single_cycle_cover = connect_cycles_recursive(cover, sig)
        for index, cycle in enumerate(single_cycle_cover):
            print(f"cycle {index} tail: {cycle[0][0][-tail_length:]}")
        print(f"scc length {recursive_cycle_check(single_cycle_cover)}")
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
        except AssertionError as e:
            print(f"List of cycles is not a valid cycle cover: {e}")
            print(
                f"Path: {pathQ(perms[0])}, Cycle: {cycleQ(perms[0])}. The expected length is {multinomial(s)}"
            )
