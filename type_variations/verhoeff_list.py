import collections
import copy
import sys
from typing import List

from path_operations import adjacent, cutCycle, spurBaseIndex
from permutation_graphs import binomial, halveSignature, rotate, permutations, stutterPermutationQ
from rivertz import SetPerm



def stutterize(s: List[int]):
    """Converts argument into stutter permutation by repeating every number."""
    return [[el for el in t for _ in range(2)] for t in s]


def selectOdds(sig: tuple):
    """Returns list of numbers with odd occurrence frequencies in the given signature."""
    return [i for i, item in enumerate(sig) if item % 2 == 1]


def stutterPermutations(s):
    """Generates stutter permutations of a given list of integers."""
    odds = selectOdds(s)
    if len(odds) >= 2:
        return []
    else:
        result = stutterize(permutations(halveSignature(s)))
        if len(odds) == 1:
            return extend(result, odds)
        else:
            return result

def createZigZagPath(c: List[tuple], u: tuple, v: tuple) -> List[List[int]]:
    """
    :param c: cycle of even length, list of tuples
    :param u: tuple to append
    :param v: tuple to append
    :return: cycle obtained by combining two "parallel" copies of given cycle, to form a 'square wave',
            running from cycle[[1]]v to cycle[[-1]]v; the two copies are distinguished by
            appending u and v; also works for a path
    """
    assert adjacent(u, v)
    temp = [item for sublist in zip(c, c) for item in sublist]
    module = [u, v, v, u]
    return [item + module[i % 4] for i, item in enumerate(temp)]


def incorporateSpurInZigZag(path, vertex_pair) -> List[List[int]]:
    # Modify path to remove last e elements except for the first one
    i = spurBaseIndex(path, vertex_pair[0])
    return path[:i+1] + vertex_pair + path[i+1:]


def incorporateSpursInZigZag(path, vertices, spur_suffixes) -> List[List[int]]:
    C = [stut+suff for stut in vertices for suff in spur_suffixes]
    for vertex_index in range(0, len(C), 2):
        path = incorporateSpurInZigZag(path, [C[vertex_index], C[vertex_index+1]])
    return path


def createSquareTube(path: List[tuple], u: tuple, v: tuple) -> List[List[int]]:
    # interleave the elements of the four copies of the path list
    temp = [item for sublist in zip(*([path]*4)) for item in sublist]
    uu = u + u
    uv = u + v
    vu = v + u
    vv = v + v
    module1 = [uu, uv, vv, vu, vu, vv, uv, uu]
    module2 = [uu, uv, vv, vu, vu, uu, uv, vv]

    # Combine the path with modules based on the index
    result = [item + module1[i % 8] for i, item in enumerate(temp[:-8])] +\
             [item + module2[i % 8] for i, item in enumerate(temp[-8:])]
    return result


def swapPair(perm, i, j=None) -> List[int]:
    """Swaps elements in perm at positions i and j (or i and i+1 if j is not provided)."""
    if j is None:
        j = i + 1
    if i < len(perm) and j < len(perm):
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def extend(lst: List[List[int]], e: List[int]) -> List[List[int]]:
    """
     Extend every item in l with e
    :param lst: list of lists of integers
    :param e: list to extend every item in l with
    :return:
    """
    try:
        return [i + e for i in lst]
    except TypeError:
        return [i + [e] for i in lst]


def HpathNS(k0: int, k1: int) -> List[List[int]]:
    odd_perms = []
    tuple_0 = k0 * [0]
    tuple_1 = k1 * [1]
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
        return [[1 if x == 0 else 0 for x in tup] for tup in HpathNS(k1, k0)]
    if k0 % 2 == 1 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), [1])  # A Hamiltonian path from 0^k0 1^k1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), [0])  # A Hamiltonian cycle from 1^(k1-1) 0^(k0-1) 1 0

        return p1[:-1] + rotate(p0, 1) + [p1[-1]]

    elif k0 % 2 == 0 and k1 % 2 == 1:
        p1 = extend(HpathNS(k0, k1 - 1), [1])  # A Hamiltonian cycle containing edge 0^(k0-1) 1^(k1-1) 0 1 ~ 0^(k0-2) 1 0 1^(k1-2) 0 1
        p0 = extend(HpathNS(k0 - 1, k1), [0])  # A Hamiltonian path from 0^(k0-1) 1^k1 0 to 1^k1 0^k1
        v = p0[0]
        return [v] + cutCycle(p1[::-1], swapPair(copy.deepcopy(v), -2)) + p0[1:]
    elif k0 % 2 == 0 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), [1])  # A Hamiltonian path from 0^(k0-1) 1^(k1-1) 0 1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), [0])
            
        if stutterPermutationQ(p0[-1]):
            p0 = p0[:-1]
        if k0 == k1: # p0 is a path from 0^(k0-1) 1^k1 0 to 1^(k1-1) 0^(k0-1) 1 0
            return p1[::-1] + p0[::-1]
        return p1[::-1] + p0
    else:
        p11 = HpathNS(k0, k1 - 2)
        p1101 = HpathNS(k0 - 1, k1 - 3)
        p0101 = HpathNS(k0 - 2, k1 - 2)
        # if k0 == k1:
        #     p0001 = [[1 if x == 0 else 0 for x in tup] for tup in p1101]
        #     p00 = [[1 if x == 0 else 0 for x in tup] for tup in p11]
        # else:
        p0001 = HpathNS(k0 - 3, k1 - 1)
        p00 = HpathNS(k0 - 2, k1)

        sp00 = extend(stutterPermutations([k0 - 3, k1 - 1]), [0, 0])
        sp11 = extend(stutterPermutations([k0 - 1, k1 - 3]), [1, 1])
        tube = createSquareTube(p0101[::-1], [0, 1], [1, 0])
        tube1, tube2, tube3 = tube[:3], tube[3:-2], tube[-2:]

        if len(p1101) == 0:
            c11xy = [stut+suff for suff in [[0, 1], [1, 0]] for stut in sp11]
        else:
            ext_path = extend(cutCycle(p1101, p0101[0][:-1] + [0]), [1, 1])
            p11xy = rotate(createZigZagPath(ext_path, [1, 0], [0, 1]), 1)
            c11xy = incorporateSpursInZigZag(p11xy, sp11, [[0, 1], [1, 0]])

        if len(p0001) == 0:
            c00xy = [stut+suff for suff in [[1, 0], [0, 1]] for stut in sp00]
        else:
            ext_path = extend(cutCycle(p0001, p0101[-1][:-1] + [1]), [0, 0])
            p00xy = rotate(createZigZagPath(ext_path, [0, 1], [1, 0]), 1)
            c00xy = incorporateSpursInZigZag(p00xy, sp00, [[1, 0], [0, 1]])

        if k0 - 2 < k1:
            p00 = p00[::-1]

        path_ham = extend(p11, [1, 1]) + tube1 + c00xy + tube2 + c11xy + tube3 + extend(p00, [0, 0])
        if len(path_ham) != len(set(tuple(row) for row in path_ham)):
            print("Path contains duplicates:", [item for item, count in collections.Counter([tuple(node) for node in path_ham]).items() if count > 1])
        if len(path_ham) < binomial(k0, k1):
            rivertz_perms = []
            for p in SetPerm([k0, k1]):
                rivertz_perms.append(p)
            corrected_tuples = [[x - 1 for x in item] for item in rivertz_perms]
            print("Path is missing elements:", [item for item in corrected_tuples if item not in path_ham])
        return path_ham
