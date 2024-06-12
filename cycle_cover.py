import argparse

import numpy as np

from helper_operations.path_operations import (
    conditionHpath,
    createZigZagPath,
    cutCycle,
    cycleQ,
    incorporateSpursInZigZag,
    pathQ,
    splitPathIn2,
    transform,
)
from helper_operations.permutation_graphs import (
    extend,
    multinomial,
    rotate,
    shorten,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma2_extended_path
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
    Generates a path based on the input signature `sig` from 1 2 0^{k2} to 0 2 1 0^{k2-1}.

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
    for i in range(0, k+1):
        bottom_path.append((2,) + k_0_tuple[:i] + (1,) + k_0_tuple[i:])
    midpath = []
    for i in range(0, k, 2):
        # construct the path going up
        up_path = (0,) + k_0_tuple[i+1:] + (1,) + k_0_tuple[1:i+1]
        for j in range(1, len(up_path)-i):
            midpath.append(up_path[:j] + (2,) + up_path[j:])
        # construct the path going left (incl top-right corner node)
        left_path = k_0_tuple[i:] + (2,) + k_0_tuple[:i]
        for j in reversed(range(0, len(left_path)-i)):
            midpath.append(left_path[:j] + (1,) + left_path[j:])
        right_path = k_0_tuple[i+1:] + (2,) + k_0_tuple[:i+1]
        # construct the path going right (incl top-right corner node)
        for j in range(0, len(right_path)-i):
            midpath.append(right_path[:j] + (1,) + right_path[j:])
        # construct the path going down
        down_path = k_0_tuple[i+1:] + (1,) + k_0_tuple[:i+1]
        for j in reversed(range(1, len(down_path)-2-i)):
            midpath.append(down_path[:j] + (2,) + down_path[j:])
    print(bottom_path + midpath)
    return bottom_path + midpath


def HpathOdd_2_1(k: int) -> list[tuple[int, ...]]:
    """
    Generates a path based on the number of 0's `k` from 1 2 0^{k0-1} 1 to 0 2 1 0^{k0-2} 1.
    @param k: The input value for k0
    @return: The generated path
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
    start_path = [
        (1, 2) + k_0_tuple + (1,),
        (2, 1) + k_0_tuple + (1,),
        (2, 0, 1) + k_0_tuple[:-1] + (1,),
        (2, 0, 0, 1) + k_0_tuple[:-2] + (1,),
        (2, 0, 0, 0, 1) + k_0_tuple[:-3] + (1,),
    ]
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
        for i in range(3, k):
            mid_path.append(
                (2,) + k_0_tuple[: i + 1] + (1,) + k_0_tuple[i + 1 :] + (1,)
            )
        for i in range(3, k, 2):
            prefix_zeros = i - 3
            print(f"{i}; prefix_zeros: {prefix_zeros}")
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


def HpathCycleCover(sig: list[int]) -> list[tuple[int, ...]]:
    # sort list in descending order
    sorted_sig = sorted(sig, reverse=True)
    if sorted_sig != sig:
        indexed_sig = [(value, idx) for idx, value in enumerate(sig)]
        indexed_sig.sort(reverse=True, key=lambda x: x[0])
        # print(f"tr: {[sig.index(x) for x in sorted_sig]}, br: {[x[0] for x in indexed_sig]}/{[x[1] for x in indexed_sig]}, sig {sig}")
        # print(f"Sig: {sig} sorted {sorted_sig}, RET {transform(HpathCycleCover(sorted_sig), [x[1] for x in indexed_sig])}")
        return transform(HpathCycleCover(sorted_sig), [x[1] for x in indexed_sig])
    k = sig[0]
    if len(sig) == 2:
        return HpathNS(sig[0], sig[1])
    elif 0 in sig:
        return HpathCycleCover(sig[:-1])
    elif len(sig) == 3 and sig[1] == 1 and sig[2] == 1:
        # Odd-1-1 AND Even-1-1 case

        # Split off the trailing number x
        p_path = HpathNS(k, 1)
        # a path from 0^k 1 2 to 1 0^k 2
        p2 = extend(p_path, (2,))
        # a path from 2 0^k 1 to 0^k 2 1
        p1 = extend([tuple(2 if x == 1 else 0 for x in tup) for tup in p_path], (1,))
        # by IH, a path/cycle from 1 0^k 2 (path to 2 0^k 1)
        p0 = extend(HpathCycleCover([k - 1, 1, 1]), (0,))

        # HpathNS is missing a node when k_0 is even, we add this back
        if k % 2 == 0:
            p2 = [tuple([0] * k) + (1, 2)] + p2
            p1 = [tuple([0] * k) + (2, 1)] + p1
        if k == 0:
            # reverse these, because sorting of signature reversed up the order
            p1 = p1[::-1]
            p0 = p0[::-1]
        print(f"sig: {sig}, p2: {p2}, p1: {p1}, p0: {p0}")
        if k % 2 == 1:
            return p2[-1:] + p0 + p1[::-1] + p2[:-1]
        else:
            # Even k, also need to add 0^k0 1 2 and 0^k0 2 1
            return p2[-1:] + p0 + p2[:-1][::-1] + p1
    elif len(sig) == 3 and k % 2 == 0 and sig[1] == 2 and sig[2] == 1:
        # even-2-1 case
        p2 = extend(HpathNS(k, 2), (2,))  # a cycle
        p1 = extend(
            transform(lemma2_extended_path(tuple([2] * k)), [1, 2, 0]), (1,)
        )  # a path from c = 1 2 0^k 1 to d = 0 2 1 0^(k-1) 1 using Stachowiak's Lemma 2
        if k == 2:
            transformed = transform(HpathAlt([2, 1, 1]), [1, 2, 0])
        else:
            transformed = HpathAlt([k - 1, 2, 1])[::-1]
        p0 = extend(
            transformed, (0,)
        )  # a path from a = 1 2 0^(k-1) 1 to b = 0 2 1 0^(k-2) 1
        # 1 2 0^{k2} to 0 2 1 0^{k2-1}.
        v = (1,) + tuple([0] * k) + (1, 2)
        c = p0 + p1
        print(f"SIG: {sig}, p2: {p2}, p1: {p1}, p0: {p0}, v: {v}")
        return cutCycle(p2, swapPair(v, 1))[::-1] + cutCycle(c, swapPair(v, -2))
    elif len(sig) == 3 and k % 2 == 1 and sig[1] == 2 and sig[2] == 1:
        # odd-2-1 case
        # p12 = extend(HpathNS(k, 1), (1, 2))
        p02 = HpathNS(k - 1, 2)  # p20 is parallel to p02
        p1 = extend(HpathCycleCover([k, 1, 1]), (1,))
        p10 = extend(HpathCycleCover([k - 1, 1, 1]), (1, 0))
        if k - 2 == 1:
            transformed = HpathOdd_2_1(1)
        else:
            transformed = HpathOdd_2_1(k - 2)[::-1]
        p00 = extend(transformed, (0, 0))
        sp02 = stutterPermutations([k - 1, 2])  # stutter permutations for p02, p20
        v1 = tuple([0] * k) + (1, 2, 1)
        v2 = (1,) + tuple([0] * k) + (2, 1)
        c0 = p10 + p00
        cns = createZigZagPath(p02, (2, 0), (0, 2))
        c2 = incorporateSpursInZigZag(cns, sp02, [(0, 2), (2, 0)])

        # 3 segments
        split1_0, split1_1 = splitPathIn2(p1, v1)
        if v1 in split1_0:
            split1_0, split1_2 = splitPathIn2(split1_0, swapPair(v2, -3))
        else:
            split1_1, split1_2 = splitPathIn2(split1_1, swapPair(v2, -3))

        p1p12 = [
            createZigZagPath(shorten(path, 2), (2, 1), (1, 2)) if i == 1 else path
            for i, path in enumerate([split1_0, split1_1, split1_2])
        ]
        print(f"p1p12: {p1p12}, path: {pathQ(p1p12)}")
        p = p1p12[:2] + rotate(c0, 2) + p1p12[2:]
        split2_0, split2_1 = splitPathIn2(p, swapPair(v2, -2))
        return split2_0 + rotate(c2, 2) + split2_1
    elif sum(1 for n in sig if n % 2 == 1) >= 2:
        # stachowiak's odd case
        pass
    elif any(n % 2 == 1 for n in sig):
        # all-but-one even case
        pass
    else:
        # all-even case
        pass


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
        print(
            f"Verhoeff's result for signature {s}: {len(set(tuple(row) for row in perms))}/{len(perms)}/{multinomial(s)} "
            f"is a path: {pathQ(perms)} and a cycle: {cycleQ(perms)}"
        )
