import argparse

from helper_operations.path_operations import (
    createZigZagPath,
    cutCycle,
    cycleQ,
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
    multinomial,
    rotate,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma11
from verhoeff import HpathNS


def Hpath_even_1_1(k: int) -> list[tuple[int, ...]]:
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


def Hpath_odd_2_1(k: int) -> list[tuple[int, ...]]:
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


def parallel_sub_cycle_odd_2_1(k: int) -> list[tuple[int, ...]]:
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


def incorporated_odd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from 1 2 0^{k0-1} 1 to 0 2 1 0^{k0-2} 1
    Including the _02 and _20 cycles (with stutters), and the _1 & _12 path.

    @param k: The input value for k0, must be odd
    @return: The generated path from a to b
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


def generate_cycle_cover(sig: list[int]) -> list[list[tuple[int, ...]]]:
    # sort list in descending order
    if len(sig) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(sig) == 1:
        return [[(0,) * sig[0]]]
    sorted_sig = sorted(sig, reverse=True)
    if sorted_sig != sig:
        if sig == [1, 2, 1]:
            return [Hpath_odd_2_1(1)]
        new_sig, transformer = get_transformer(sig, lambda x: x[0])
        return transform_cycle_cover(generate_cycle_cover(new_sig), transformer)
    k = sig[0]
    if len(sig) == 2:
        return [HpathNS(sig[0], sig[1])]
    elif 0 in sig:
        return generate_cycle_cover(sig[:-1])
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
        p0 = extend(generate_cycle_cover([k - 1, 1, 1])[0], (0,))

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
            Hpath_even_1_1(k),
            (1,),
        )  # a path from c = 1 2 0^k 1 to d = 0 2 1 0^(k-1) 1
        p0 = extend(
            generate_cycle_cover([k - 1, 2, 1])[0][::-1], (0,)
        )  # a path from b0 = 0 2 1 0^(k-2) 1 0 to a0 = 1 2 0^(k-1) 1 0
        # 1 2 0^{k2} to 0 2 1 0^{k2-1}.
        v = (1,) + tuple([0] * k) + (1, 2)
        c = p0 + p1
        return [cutCycle(p2, swapPair(v, 1))[::-1] + cutCycle(c, swapPair(v, -2))]
    # odd-2-1 case
    elif len(sig) == 3 and k % 2 == 1 and sig[1] == 2 and sig[2] == 1:
        # the path from a to b (_1 | _12) with parallel 02-20 cycles incorporated
        p1_p12_p02_p20 = incorporated_odd_2_1(k)
        # path from c'10=120^{k_0-1}10 to d'10=0210^{k_0-1}10 (_10)
        p10 = extend(Hpath_even_1_1(k - 1), (1, 0))
        # path from a'00=120^{k_0-2}100 to b'00=0210^{k_0-3}100 (_00)
        p00 = extend(generate_cycle_cover([k - 2, 2, 1])[0], (0, 0))
        cycle = rotate(p10 + p00[::-1], 1)[::-1]
        # b = 0 2 1 0^(k-2) 1 to a = 1 2 0^(k-1) 1
        return [p1_p12_p02_p20[:1] + cycle + p1_p12_p02_p20[1:]]
    # stachowiak's odd case
    elif sum(1 for n in sig if n % 2 == 1) >= 2:
        new_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])
        return [transform(lemma11(new_sig), transformer)]
    # all-but-one even case
    elif any(n % 2 == 1 for n in sig):
        all_sub_cycles = []
        for idx, color in enumerate(sig):
            sub_sig = sig[:idx] + [color - 1] + sig[idx + 1 :]
            # check if this results an odd-2-1 case, then we need a cycle and not a path
            sorted_sub_sig, transformer = get_transformer(
                sub_sig, lambda x: [x[0] % 2, x[0]]
            )
            if (
                sorted_sub_sig[0] % 2 == 1
                and sorted_sub_sig[1] == 1
                and sorted_sub_sig[2] == 2
            ):
                c = [transform(lemma11(sorted_sub_sig), transformer)]
            else:
                c = generate_cycle_cover(sub_sig)
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
                sorted_sub_sig, transformer = get_transformer(sub_sig, lambda x: x[0])
                # for the even-1-1 case we need a specific path that has parallel edges
                if (
                    sorted_sub_sig[0] % 2 == 0
                    and sorted_sub_sig[1] == 1
                    and sorted_sub_sig[2] == 1
                ):
                    cycle_cover = [
                        transform(
                            Hpath_even_1_1(sorted_sub_sig[0]),
                            transformer,
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
                else:
                    # this gives all the non-stutter permutations
                    sub_cycles = extend_cycle_cover(cycle_cover, (idx, idx2))
                all_sub_cycles.append(sub_cycles)
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
    s = [int(x) for x in args.signature.split(",")]
    if len(s) > 1:
        perms = generate_cycle_cover(s)
        if args.verbose:
            print(f"Resulting path {perms}")
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
