import copy
import sys

from helper_operations.path_operations import adjacent, cutCycle, spurBaseIndex
from helper_operations.permutation_graphs import (
    halve_signature,
    permutations_from_sig,
    rotate,
)


def stutterize(p: list[int]) -> list[list[int]]:
    """
    Converts argument into a stutter permutation by repeating every number.

    Args:
        p (list[int]): permutation as a list of integers

    Returns:
        list[list[int]]: every number in p repeated twice and put into a list
    """
    return [[el for el in t for _ in range(2)] for t in p]


def selectOdds(sig: tuple[int, ...]) -> list[int]:
    """
    Returns list of numbers with odd occurrence frequencies in the given signature.
    Args:
        sig (tuple[int, ...]): signature as a list of integers
    Returns:
        list[int]: list of integers with odd occurrence frequencies in the signature
    """
    return [i for i, item in enumerate(sig) if item % 2 == 1]


def stutterPermutations(s: tuple[int, ...]) -> list[list[int]]:
    """
    Generates stutter permutations of a given signature.
    Stutter permutations have the form [a, a, b, b, c, c, ..., z] where a, b, c, ... are the elements of the permutation.
    So every pair of elements is repeated twice from the left. An stutter can have one element with odd frequency appended at the end.
    Args:
        s (tuple[int, ...]): the signature of the stutter permutations
    Returns:
        list[list[int]]: list of stutter permutations of signature `s`
    """
    odds = selectOdds(s)
    if len(odds) >= 2:
        return []
    else:
        result = stutterize(permutations_from_sig(halve_signature(s)))
        if len(odds) == 1:
            return extend(result, odds)
        else:
            return result


def createZigZagPath(c: list[list[int]], u: list[int], v: list[int]) -> list[list[int]]:
    """
    Creates a zigzag path from a given cycle `c` by appending `u` and `v` and `v` and `u` alternatively.
    Args:
        c (list[list[int]]): cycle of even length, list of tuples of integers
        u (list[int]): tuple to append
        v (list[int]): tuple to append, adjacent to `u`
    Returns:
        list[list[int]]:
            cycle obtained by combining two "parallel" copies of given cycle, to form a 'square wave',
            running from cycle[[0]]v to cycle[[-1]]v; the two copies are distinguished by appending u and v; also works for a path
    Raises:
        AssertionError: If `u` and `v` are not adjacent
    """
    assert adjacent(u, v)
    temp = [item for sublist in zip(c, c) for item in sublist]
    module = [u, v, v, u]
    return [item + module[i % 4] for i, item in enumerate(temp)]


def incorporateSpurInZigZag(
    path: list[list[int]], vertex_pair: list[list[int]]
) -> list[list[int]]:
    """
    Incorporates a spur path into a zigzag path. The spur has the same last two elements as the zigzag path.
    The spurs are stutters if the last two elements are disregarded. They have to be incorporated in the zigzag path because those elements are appended.
    Args:
        path (list[list[int]]): zigzag path as a list of lists of integers
        vertex_pair (list[list[int]]): spur path as a list of lists of integers
    Returns:
        list[list[int]]: zigzag path with the spur path incorporated
    """
    i = spurBaseIndex(path, vertex_pair[0])
    return path[: i + 1] + vertex_pair + path[i + 1 :]


def incorporateSpursInZigZag(
    path: list[list[int]], vertices: list[list[int]], spur_suffixes: list[list[int]]
) -> list[list[int]]:
    """
    Incorporates multiple spur paths into a zigzag path. Uses the `incorporateSpurInZigZag` function.
    Args:
        path (list[list[int]]): zigzag path as a list of lists of integers.
        vertices (list[list[int]]): list of spur paths as a list of lists of integers.
        spur_suffixes (list[list[int]]): list of suffixes for the spur paths.
    Returns:
        list[list[int]]: zigzag path with the spur paths incorporated.
    """
    C = [stut + suff for stut in vertices for suff in spur_suffixes]
    for vertex_index in range(0, len(C), 2):
        path = incorporateSpurInZigZag(path, [C[vertex_index], C[vertex_index + 1]])
    return path


def createSquareTube(
    path: list[list[int]], u: list[int], v: list[int]
) -> list[list[int]]:
    """
    Creates a square tube from a given path by appending `u` and `v` in the following order:
    `uu`, `uv`, `vv`, `vu`, -> next node -> `vu`, `vv`, `uv`, `uu`.
    and for the last two nodes: `uu`, `uv`, `vv`, `vu` -> next node -> `vu`, `uu`, `uv`, `vv`.
    Args:
        path (list[list[int]]): path as a list of lists of integers
        u (list[int]): tuple to append
        v (list[int]): tuple to append, adjacent to `u`
    Returns:
        list[list[int]]:
            path obtained by combining four copies of given path, to form a 'square tube',
            running from `path[0]uu` to `path[-1]vv`; the four copies are distinguished by appending `u` and `v`
    """
    # interleave the elements of the four copies of the path list
    temp = [item for sublist in zip(*([path] * 4)) for item in sublist]
    uu = u + u
    uv = u + v
    vu = v + u
    vv = v + v
    module1 = [uu, uv, vv, vu, vu, vv, uv, uu]
    module2 = [uu, uv, vv, vu, vu, uu, uv, vv]

    # Combine the path with modules based on the index
    result = [item + module1[i % 8] for i, item in enumerate(temp[:-8])] + [
        item + module2[i % 8] for i, item in enumerate(temp[-8:])
    ]
    return result


def swapPair(perm: list[int], i: int, j: int | None = None) -> list[int]:
    """
    Swaps elements in perm at positions `i` and `j` (or `i` and `i+1` if `j` is not provided).
    Args:
        perm (list[int]): list of integers
        i (int): index of the first element to swap
        j (int | None, optional): index of the second element to swap. Defaults to None; in this case, `j` is set to `i+1`.
    Returns:
        list[int]: list of integers with elements at positions `i` and `j` swapped
    """
    if j is None:
        j = i + 1
    if i < len(perm) and j < len(perm):
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def extend(lst: list[list[int]], e: list[int]) -> list[list[int]]:
    """
    Extend every item in l with e
    Args:
        lst (list[list[int]]): list of lists of integers
        e (list[int]): list to extend every item in `lst` with
    Returns:
        list[list[int]]: list of lists of integers with every item of `lst` extended by `e`
    """
    try:
        return [i + e for i in lst]
    except TypeError:
        return [i + [e] for i in lst]


def HpathNS(k0: int, k1: int) -> list[list[int]]:
    """
    Computes a Hamiltonian path in the neighbor-swap graph on the non-stutter permutations for the given signature.
    If k0 and k1 are both even, the path is a Hamiltonian cycle.
    Args:
        k0 (int): Number of 0s in the signature.
        k1 (int): Number of 1s in the signature.
    Returns:
        list[list[int]]: A Hamiltonian path in the neighbor-swap graph G(0^k_0|1^(k_1)).
    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """
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
        p1 = extend(
            HpathNS(k0, k1 - 1), [1]
        )  # A Hamiltonian path from 0^k0 1^k1 to 1^(k1-1) 0^k0 1
        p0 = extend(
            HpathNS(k0 - 1, k1), [0]
        )  # A Hamiltonian cycle from 1^(k1-1) 0^(k0-1) 1 0

        return p1[:-1] + rotate(p0, 1) + [p1[-1]]

    elif k0 % 2 == 0 and k1 % 2 == 1:
        p1 = extend(
            HpathNS(k0, k1 - 1), [1]
        )  # A Hamiltonian cycle containing edge 0^(k0-1) 1^(k1-1) 0 1 ~ 0^(k0-2) 1 0 1^(k1-2) 0 1
        p0 = extend(
            HpathNS(k0 - 1, k1), [0]
        )  # A Hamiltonian path from 0^(k0-1) 1^k1 0 to 1^k1 0^k1
        v = p0[0]
        return [v] + cutCycle(p1[::-1], swapPair(copy.deepcopy(v), -2)) + p0[1:]
    elif k0 % 2 == 0 and k1 % 2 == 0:
        p1 = extend(
            HpathNS(k0, k1 - 1), [1]
        )  # A Hamiltonian path from 0^(k0-1) 1^(k1-1) 0 1 to 1^(k1-1) 0^k0 1
        p0 = extend(HpathNS(k0 - 1, k1), [0])

        if k0 == k1:  # p0 is a path from 0^(k0-1) 1^k1 0 to 1^(k1-1) 0^(k0-1) 1 0
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
            c11xy = [stut + suff for suff in [[0, 1], [1, 0]] for stut in sp11]
        else:
            ext_path = extend(cutCycle(p1101, p0101[0][:-1] + [0]), [1, 1])
            p11xy = rotate(createZigZagPath(ext_path, [1, 0], [0, 1]), 1)
            c11xy = incorporateSpursInZigZag(p11xy, sp11, [[0, 1], [1, 0]])

        if len(p0001) == 0:
            c00xy = [stut + suff for suff in [[1, 0], [0, 1]] for stut in sp00]
        else:
            ext_path = extend(cutCycle(p0001, p0101[-1][:-1] + [1]), [0, 0])
            p00xy = rotate(createZigZagPath(ext_path, [0, 1], [1, 0]), 1)
            c00xy = incorporateSpursInZigZag(p00xy, sp00, [[1, 0], [0, 1]])

        if k0 - 2 < k1:
            p00 = p00[::-1]

        path_ham = (
            extend(p11, [1, 1])
            + tube1
            + c00xy
            + tube2
            + c11xy
            + tube3
            + extend(p00, [0, 0])
        )
        return path_ham
