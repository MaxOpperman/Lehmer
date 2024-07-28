import argparse

from helper_operations.path_operations import (
    createZigZagPath,
    cutCycle,
    cycleQ,
    get_first_element,
    get_transformer,
    incorporateSpursInZigZag,
    pathQ,
    recursive_cycle_check,
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
from stachowiak import lemma2_cycle, lemma2_extended_path, lemma11
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


def generate_cycle_cover(sig: tuple[int]) -> list[list[tuple[int, ...]]]:
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
        sig (tuple[int]): The signature of the permutations. Must have at least one element.

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
        lemma2_stachowiak = lemma2_extended_path(tuple([2] * k))
        transformed_lemma2 = transform(lemma2_stachowiak, [2, 1, 0])
        return [lemma11((k, 1, 1))]
    # even-2-1 case
    elif len(list(sig)) == 3 and k % 2 == 0 and sig[1] == 2 and sig[2] == 1:
        # a cycle from 1 0^(k-1) 1 0 2 to 1 0^k 1 2
        p2 = extend(HpathNS(k, 2), (2,))[::-1]

        # p0 and p1 are combined into a cycle
        # a path from c1 = 1 2 0^k 1 to d1 = 0 2 1 0^(k-1) 1
        p1 = extend(Hpath_even_1_1(k), (1,))
        # a path from b0 = 0 2 1 0^(k-2) 1 0 to a0 = 1 2 0^(k-1) 1 0
        p0 = extend(generate_cycle_cover((k - 1, 2, 1))[0][::-1], (0,))

        # v = 1 0^(k-1) 1 2
        v = (1,) + tuple([0] * k) + (1, 2)
        c = p0 + p1
        return [cutCycle(p2, swapPair(v, 1))[::-1] + cutCycle(c, swapPair(v, -2))]
    # odd-2-1 case
    elif len(list(sig)) == 3 and k % 2 == 1 and sig[1] == 2 and sig[2] == 1:
        # the path from a to b (_1 | _12) with parallel 02-20 cycles incorporated
        p1_p12_p02_p20 = incorporated_odd_2_1(k)
        # path from c'10=120^{k_0-1}10 to d'10=0210^{k_0-1}10 (_10)
        p10 = extend(Hpath_even_1_1(k - 1), (1, 0))
        # path from a'00=120^{k_0-2}100 to b'00=0210^{k_0-3}100 (_00)
        p00 = extend(generate_cycle_cover((k - 2, 2, 1))[0], (0, 0))
        cycle = rotate(p10 + p00[::-1], 1)[::-1]
        # b = 0 2 1 0^(k-2) 1 to a = 1 2 0^(k-1) 1
        return [p1_p12_p02_p20[:1] + cycle + p1_p12_p02_p20[1:]]
    # stachowiak's odd case
    elif sum(1 for n in sig if n % 2 == 1) >= 2:
        new_sig, transformer_stachowiak = get_transformer(
            sig, lambda x: [x[0] % 2, x[0]]
        )
        return [transform(lemma11(new_sig), transformer_stachowiak)]
    # all-but-one even case
    elif any(n % 2 == 1 for n in sig):
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
                    for cyc in cycle_cover:
                        sub_cycles.append(
                            extend(cyc, (idx2, idx))[::-1] + extend(cyc, (idx, idx2))
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
                        while len(between_cycles) > 0 and idx == max(
                            get_first_element(between_cycles)[-2:]
                        ) and max(get_first_element(between_cycles, -1)[-2:]) == idx:
                            print(f"REVERSE adding between cycles {len(sub_sig)} {get_perm_signature(get_first_element(between_cycles))} {get_first_element(between_cycles)[-2:]}")
                            all_sub_cycles.append(between_cycles.pop(-1))
                    else:
                        # add the between cycles in normal order
                        while len(between_cycles) > 0 and idx == max(
                            get_first_element(between_cycles)[-2:]
                        ):
                            print(f"adding between cycles {len(sub_sig)} {get_perm_signature(get_first_element(between_cycles))} {get_first_element(between_cycles)[-2:]}")
                            all_sub_cycles.append(between_cycles.pop(0))
        if len(between_cycles) > 0:
            all_sub_cycles.append(between_cycles.pop(0))
        return all_sub_cycles


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
            print(f"Path: {pathQ(perms[0])}, Cycle: {cycleQ(perms[0])}")
