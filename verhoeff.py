import collections
import sys
from typing import List

from path_operations import conditionHpath, createSquareTube, createZigZagPath, cutCycle, incorporateSpursInZigZag, transform
from permutation_graphs import binomial, extend, rotate, stutterPermutationQ, stutterPermutations, swapPair
from rivertz import SetPerm


def HpathNS(k0: int, k1: int) -> list:
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
        p1 = extend(HpathNS(k0, k1 - 1), (1,))  # A Hamiltonian path from 0^k0 1^k1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))  # A Hamiltonian cycle from 1^(k1-1) 0^(k0-1) 1 0

        return p1[:-1] + rotate(p0, 1) + [p1[-1]]

    elif k0 % 2 == 0 and k1 % 2 == 1:
        p1 = extend(HpathNS(k0, k1 - 1), (1,))  # A Hamiltonian cycle containing edge 0^(k0-1) 1^(k1-1) 0 1 ~ 0^(k0-2) 1 0 1^(k1-2) 0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))  # A Hamiltonian path from 0^(k0-1) 1^k1 0 to 1^k1 0^k1
        v = p0[0]

        return [v] + cutCycle(p1[::-1], swapPair(v, -2)) + p0[1:]
    elif k0 % 2 == 0 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), (1,))  # A Hamiltonian path from 0^(k0-1) 1^(k1-1) 0 1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), (0,))
            
        if stutterPermutationQ(p0[-1]):
            p0 = p0[:-1]
        if k0 == k1: # p0 is a path from 0^(k0-1) 1^k1 0 to 1^(k1-1) 0^(k0-1) 1 0
            return p1[::-1] + p0[::-1]
        return p1[::-1] + p0
    else:
        p11 = HpathNS(k0, k1 - 2)
        p1101 = HpathNS(k0 - 1, k1 - 3)
        p0101 = HpathNS(k0 - 2, k1 - 2)
        p0001 = HpathNS(k0 - 3, k1 - 1)
        p00 = HpathNS(k0 - 2, k1)

        sp00 = extend(stutterPermutations([k0 - 3, k1 - 1]), (0, 0))
        sp11 = extend(stutterPermutations([k0 - 1, k1 - 3]), (1, 1))
        tube = createSquareTube(p0101[::-1], (0, 1), (1, 0))
        tube1, tube2, tube3 = tube[:3], tube[3:-2], tube[-2:]

        if len(p1101) == 0:
            c11xy = [stut+suff for suff in [(0, 1), (1, 0)] for stut in sp11]
        else:
            ext_path = extend(cutCycle(p1101, p0101[0][:-1] + (0,)), (1, 1))
            p11xy = rotate(createZigZagPath(ext_path, (1, 0), (0, 1)), 1)
            c11xy = incorporateSpursInZigZag(p11xy, sp11, [(0, 1), (1, 0)])

        if len(p0001) == 0:
            c00xy = [stut+suff for suff in [(1, 0), (0, 1)] for stut in sp00]
        else:
            ext_path = extend(cutCycle(p0001, p0101[-1][:-1] + (1,)), (0, 0))
            p00xy = rotate(createZigZagPath(ext_path, (0, 1), (1, 0)), 1)
            c00xy = incorporateSpursInZigZag(p00xy, sp00, [(1, 0), (0, 1)])

        if k0 - 2 < k1:
            p00 = p00[::-1]

        path_ham = extend(p11, (1, 1)) + tube1 + c00xy + tube2 + c11xy + tube3 + extend(p00, (0, 0))
        if len(path_ham) != len(set(path_ham)):
            print("Path contains duplicates:", [item for item, count in collections.Counter(path_ham).items() if count > 1])
        if len(path_ham) < binomial(k0, k1):
            rivertz_perms = []
            for p in SetPerm([k0, k1]):
                rivertz_perms.append(p)
            corrected_tuples = [tuple([x - 1 for x in item]) for item in rivertz_perms]
            print("Path is missing elements:", [item for item in corrected_tuples if item not in path_ham])
        return path_ham


def Hpath(*s):
    """Returns a Hamiltonian path of signature s"""
    if not conditionHpath(s):
        return None
    elif sorted(s, reverse=True) != list(s):
        list_s = list(s)
        list_s.sort(reverse=True)
        return transform(Hpath(*list_s), [i for i in sorted(range(len(list_s)), key=lambda x: list_s[x], reverse=True)])
    elif s[-1] == 0:
        return Hpath(*s[:-1])
    elif len(s) == 0:
        return []
    elif len(s) == 1:
        return [tuple(list(range(s[0])))]
    elif len(s) == 2 and s[1] == 1:
        return [tuple([1 if i == j else 0 for i in range(s[0], -1, -1)]) for j in range(s[0], -1, -1)]
    else:
        return [tuple(s)]


def HpathAlt(sig: List[int]) -> List[tuple]:
    """
    Generates a path based on the input signature `sig` from 1 2 0^{k2} to 0 2 1 0^{k2-1}.

    Args:
        sig (List[int]): The input signature.

    Returns:
        List[tuple]: The generated path.

    Raises:
        ValueError: If `k2` is not 2, 3, or greater than or equal to 4.
    """
    k2 = sig[2]
    if k2 == 2:
        p2 = extend(Hpath(2, 1, 0), (2,))
        p1 = extend([tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(2, 0, 1)], (1,))
        return [(1, 2, 0, 0), (2, 1, 0, 0), (2, 0 ,1, 0)] + p1 + p2[::-1] + [(1, 0, 2, 0), (0, 1, 2, 0), (0, 2, 1, 0)]
    elif k2 == 3:
        p2 = extend(Hpath(3, 1, 0), (2,))
        p1 = extend([tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(3, 0, 1)], (1,))
        return [(1, 2, 0, 0, 0), (2, 1, 0, 0, 0), (2, 0 ,1, 0, 0), (2, 0, 0, 1, 0)] + list(reversed(p1)) + p2 + [(1, 0, 0, 2, 0), (1, 0, 2, 0, 0), (0, 1, 2, 0, 0), (0, 1, 0, 2, 0), (0, 0, 1, 2, 0), (0, 0, 2, 1, 0), (0, 2, 0, 1, 0), (0, 2, 1, 0, 0)]
    elif k2 >= 4:
        p2 = extend(Hpath(k2, 1, 0), (2,))
        p1 = extend([tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(k2, 0, 1)], (1,))
        p20 = extend(Hpath(k2-1, 1, 0), (2, 0))
        p10 = extend([tuple([2 if i == 1 else i for i in tup]) for tup in Hpath(k2-1, 0, 1)], (1, 0))
        # by ind. hyp. a path from 1 2 0^(k-2) to 0 2 1 0^(k-3)
        p00 = extend(HpathAlt(sig[:2] + [sig[2]-2]), (0, 0))
        return p00[:k2] + [p10[0]] + p1 + p2[::-1] + p20 + p10[1:][::-1] + p00[k2:]
    else:
        raise ValueError("k must be 2, 3 or greater than or equal to 4")
