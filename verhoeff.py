import collections
import sys

from helper_operations.path_operations import (
    createSquareTube,
    createZigZagPath,
    cutCycle,
    incorporateSpursInZigZag,
)
from helper_operations.permutation_graphs import (
    binomial,
    extend,
    rotate,
    stutterPermutationQ,
    stutterPermutations,
    swapPair,
)
from rivertz import SetPerm


def HpathNS(k0: int, k1: int) -> list[tuple[int, ...]]:
    odd_perms = []
    tuple_0 = tuple(k0 * [0])
    tuple_1 = tuple(k1 * [1])
    sys.setrecursionlimit(2500)
    if k0 == 0:
        if k1 % 2 == 0:
            return []
        return [tuple_1]
    elif k1 == 0:
        if k0 % 2 == 0:
            return []
        return [tuple_0]
    elif k1 == 1:
        # path from 1^k1 0 to 0 1^k1, if k0 odd, else from 1^(k1-1) 0 1 to 0 1^k1
        for i in reversed(range(k0 + 1)):
            odd_perms.append(tuple_0[:i] + tuple_1 + tuple_0[i:])
        return odd_perms if k0 % 2 else odd_perms[1:]
    elif k0 == 1:
        # path from 0^k0 1 to 1 0^k0, if k1 odd, else from 0^(k0-1) 1 0 to 1 0^k0
        for i in reversed(range(k1 + 1)):
            odd_perms.append(tuple_1[:i] + tuple_0 + tuple_1[i:])
        return odd_perms if k1 % 2 else odd_perms[1:]
    if k0 < k1:
        return [tuple(1 if x == 0 else 0 for x in tup) for tup in HpathNS(k1, k0)]
    if k0 % 2 == 1 and k1 % 2 == 0:
        p1 = extend(
            HpathNS(k0, k1 - 1), (1,)
        )  # A Hamiltonian path from 0^k0 1^k1 to 1^(k1-1) 0^k0 1
        p0 = extend(
            HpathNS(k0 - 1, k1), (0,)
        )  # A Hamiltonian cycle from 1^(k1-1) 0^(k0-1) 1 0

        return p1[:-1] + rotate(p0, 1) + [p1[-1]]

    elif k0 % 2 == 0 and k1 % 2 == 1:
        p1 = extend(
            HpathNS(k0, k1 - 1), (1,)
        )  # A Hamiltonian cycle containing edge 0^(k0-1) 1^(k1-1) 0 1 ~ 0^(k0-2) 1 0 1^(k1-2) 0 1
        p0 = extend(
            HpathNS(k0 - 1, k1), (0,)
        )  # A Hamiltonian path from 0^(k0-1) 1^k1 0 to 1^k1 0^k1
        v = p0[0]

        return [v] + cutCycle(p1[::-1], swapPair(v, -2)) + p0[1:]
    elif k0 % 2 == 0 and k1 % 2 == 0:
        p1 = extend(
            HpathNS(k0, k1 - 1), (1,)
        )  # A Hamiltonian path from 0^(k0-1) 1^(k1-1) 0 1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))

        if stutterPermutationQ(p0[-1]):
            p0 = p0[:-1]
        if k0 == k1:  # p0 is a path from 0^(k0-1) 1^k1 0 to 1^(k1-1) 0^(k0-1) 1 0
            return p1[::-1] + p0[::-1]
        return p1[::-1] + p0
    else:
        p11 = HpathNS(k0, k1 - 2)
        p1101 = HpathNS(k0 - 1, k1 - 3)
        p0101 = HpathNS(k0 - 2, k1 - 2)
        if k0 == k1:
            p0001 = [tuple([1 if x == 0 else 0 for x in tup]) for tup in p1101]
            p00 = [tuple([1 if x == 0 else 0 for x in tup]) for tup in p11]
        else:
            p0001 = HpathNS(k0 - 3, k1 - 1)
            p00 = HpathNS(k0 - 2, k1)

        sp00 = extend(stutterPermutations([k0 - 3, k1 - 1]), (0, 0))
        sp11 = extend(stutterPermutations([k0 - 1, k1 - 3]), (1, 1))
        tube = createSquareTube(p0101[::-1], (0, 1), (1, 0))
        tube1, tube2, tube3 = tube[:3], tube[3:-2], tube[-2:]

        if len(p1101) == 0:
            c11xy = [stut + suff for suff in [(0, 1), (1, 0)] for stut in sp11]
        else:
            ext_path = extend(cutCycle(p1101, p0101[0][:-1] + (0,)), (1, 1))
            p11xy = rotate(createZigZagPath(ext_path, (1, 0), (0, 1)), 1)
            c11xy = incorporateSpursInZigZag(p11xy, sp11, [(0, 1), (1, 0)])

        if len(p0001) == 0:
            c00xy = [stut + suff for suff in [(1, 0), (0, 1)] for stut in sp00]
        else:
            ext_path = extend(cutCycle(p0001, p0101[-1][:-1] + (1,)), (0, 0))
            p00xy = rotate(createZigZagPath(ext_path, (0, 1), (1, 0)), 1)
            c00xy = incorporateSpursInZigZag(p00xy, sp00, [(1, 0), (0, 1)])

        if k0 - 2 < k1:
            p00 = p00[::-1]

        path_ham = (
            extend(p11, (1, 1))
            + tube1
            + c00xy
            + tube2
            + c11xy
            + tube3
            + extend(p00, (0, 0))
        )
        if len(path_ham) != len(set(path_ham)):
            print(
                "Path contains duplicates:",
                [
                    item
                    for item, count in collections.Counter(path_ham).items()
                    if count > 1
                ],
            )
        if len(path_ham) < binomial(k0, k1):
            rivertz_perms = []
            for p in SetPerm([k0, k1]):
                rivertz_perms.append(p)
            corrected_tuples = [tuple([x - 1 for x in item]) for item in rivertz_perms]
            print(
                "Path is missing elements:",
                [item for item in corrected_tuples if item not in path_ham],
            )
        return path_ham
